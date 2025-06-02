from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pathlib import Path
import os
from PIL import Image as PILImage
from models import Factura
from utils import format_currency
from datetime import datetime
from typing import Optional # Import Optional for type hinting

class InvoiceCanvas(canvas.Canvas):
    """Canvas personalizado para añadir marca de agua"""
    
    def __init__(self, *args, **kwargs):
        self.logo_path = kwargs.pop('logo_path', None)
        canvas.Canvas.__init__(self, *args, **kwargs)
    
    def showPage(self):
        """Añade la marca de agua antes de mostrar la página"""
        if self.logo_path and os.path.exists(self.logo_path):
            self.add_watermark()
        canvas.Canvas.showPage(self)
    
    def add_watermark(self):
        """Añade el logo como marca de agua"""
        try:
            # Configurar la opacidad y posición
            self.saveState()
            
            # Obtener dimensiones de la página
            page_width, page_height = letter
            
            # Cargar la imagen y redimensionarla para la marca de agua
            img = ImageReader(self.logo_path)
            img_width, img_height = img.getSize()
            
            # Escalar la imagen para que sea visible pero no intrusiva
            scale_factor = 0.5 # Adjusted from 0.3 to 0.5 to make the logo bigger
            display_width = img_width * scale_factor
            display_height = img_height * scale_factor
            
            # Posicionar la marca de agua en el centro de la página
            x = (page_width - display_width) / 2
            y = (page_height - display_height) / 2
            
            self.setFillAlpha(0.1) # Opacidad (0.0 a 1.0)
            self.drawImage(img, x, y, width=display_width, height=display_height, mask='auto')
            self.restoreState()
        except Exception as e:
            print(f"Error al añadir marca de agua: {e}")

def generate_invoice_pdf(factura: Factura, output_path: str, logo_path: Optional[str] = None):
    """
    Genera un archivo PDF de factura.
    Args:
        factura (Factura): Objeto Factura con todos los detalles.
        output_path (str): Ruta donde se guardará el PDF.
        logo_path (Optional[str]): Ruta al logo preparado para usar como marca de agua.
    """
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- Company Data (New Addition) ---
    company_name = "LUXBEAUTY LAB"
    company_nit = "900.123.456-7"
    company_address = "Calle ITM 123, Ciudad Medellín team Store"
    company_phone = "(57) 300 000 0000"
    company_email = "alvaro@luxbeautylab.com"

    # Define styles for company info
    company_name_style = ParagraphStyle(
        'CompanyName',
        parent=styles['h2'],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4A90E2"), # A nice blue color
        fontSize=18,
        spaceAfter=6
    )
    company_info_style = ParagraphStyle(
        'CompanyInfo',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        spaceAfter=3
    )

    story.append(Paragraph(company_name, company_name_style))
    story.append(Paragraph(f"NIT: {company_nit}", company_info_style))
    story.append(Paragraph(company_address, company_info_style))
    story.append(Paragraph(f"Teléfono: {company_phone}", company_info_style))
    story.append(Paragraph(f"Email: {company_email}", company_info_style))
    story.append(Spacer(1, 12)) # Add some space after company info

    # --- Invoice Header ---
    header_data = [
        [Paragraph(f"**FACTURA DE VENTA**<br/><font size='14'>{factura.numero}</font>", styles['h2']),
         Paragraph(f"**Fecha:** {factura.fecha.strftime('%d/%m/%Y')}", styles['Normal'])]
    ]
    header_table = Table(header_data, colWidths=[4.5*inch, 2.5*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))

    # --- Client Information ---
    client_data = [
        [Paragraph("<b>Información del Cliente:</b>", styles['Normal'])],
        [Paragraph(f"<b>Nombre:</b> {factura.cliente.nombre}", styles['Normal'])],
        [Paragraph(f"<b>Documento:</b> {factura.cliente.documento}", styles['Normal'])],
        [Paragraph(f"<b>Teléfono:</b> {factura.cliente.telefono}", styles['Normal'])],
        [Paragraph(f"<b>Email:</b> {factura.cliente.email}", styles['Normal'])],
        [Paragraph(f"<b>Dirección:</b> {factura.cliente.direccion}", styles['Normal'])]
    ]
    client_table = Table(client_data, colWidths=[7*inch])
    client_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 12))

    # --- Items Table ---
    data = [[
        Paragraph("<b>Código</b>", styles['Normal']),
        Paragraph("<b>Descripción</b>", styles['Normal']),
        Paragraph("<b>Cant.</b>", styles['Normal']),
        Paragraph("<b>P. Unit.</b>", styles['Normal']),
        Paragraph("<b>Desc. (%)</b>", styles['Normal']),
        Paragraph("<b>IVA (%)</b>", styles['Normal']),
        Paragraph("<b>Subtotal</b>", styles['Normal']),
        Paragraph("<b>Total</b>", styles['Normal'])
    ]]
    for item in factura.items:
        item_code = item.producto.codigo if item.producto else item.servicio.codigo
        item_description = item.producto.nombre if item.producto else item.servicio.nombre
        data.append([
            Paragraph(item_code, styles['Normal']),
            Paragraph(item_description, styles['Normal']),
            Paragraph(str(item.cantidad), styles['Normal']),
            Paragraph(format_currency(item.precio_unitario), styles['Normal']),
            Paragraph(f"{item.descuento:.1f}%", styles['Normal']),
            Paragraph(f"{item.iva:.1f}%", styles['Normal']),
            Paragraph(format_currency(item.subtotal()), styles['Normal']),
            Paragraph(format_currency(item.total()), styles['Normal'])
        ])

    item_table = Table(data, colWidths=[0.8*inch, 2.2*inch, 0.5*inch, 1*inch, 0.7*inch, 0.6*inch, 0.8*inch, 0.8*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E0E0E0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'), # Align description to left
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(item_table)
    story.append(Spacer(1, 12))

    # --- Totals Section ---
    totals_data = [
        ["Subtotal:", format_currency(factura.subtotal)],
        ["Descuento Total:", format_currency(factura.descuento_total)],
        ["IVA Total:", format_currency(factura.iva_total)],
        ["Total a Pagar:", format_currency(factura.total)]
    ]
    totals_table = Table(totals_data, colWidths=[5.5*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,3), (-1,3), 'Helvetica-Bold'), # Total row bold
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 12))

    # --- Payment Method and Observations ---
    story.append(Paragraph(f"<b>Medio de Pago:</b> {factura.medio_pago.value}", styles['Normal']))
    if factura.observaciones:
        story.append(Paragraph(f"<b>Observaciones:</b> {factura.observaciones}", styles['Normal']))
    story.append(Spacer(1, 30))
    
    # --- Footer ---
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph("Gracias por su compra", footer_style))
    story.append(Paragraph("LUXBEAUTY LAB - Sistema de Facturación", footer_style))
    
    # Build the PDF
    # Use the custom canvas to add watermark if logo_path is provided
    if logo_path:
        doc.build(story, canvasmaker=lambda *args, **kwargs: InvoiceCanvas(*args, logo_path=logo_path, **kwargs))
    else:
        doc.build(story)
    
    print(f"Factura PDF generada: {output_path}")

# Auxiliary function to prepare the logo
def prepare_logo(logo_path: str, output_path: str = "assets/logo_prepared.png"):
    """
    Prepara el logo para usar como marca de agua optimizando su formato.
    Convierte a PNG y redimensiona si es necesario.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Open and process the image
        with PILImage.open(logo_path) as img:
            # Convert to RGBA if not already (for handling transparency)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize if very large (optimization)
            max_size = (800, 800) # Max dimensions for the prepared logo
            img.thumbnail(max_size, PILImage.Resampling.LANCZOS) # Use LANCZOS for high quality downsampling
            
            img.save(output_path, format='PNG') # Save as PNG for better transparency handling in PDFs
        
        print(f"Logo preparado y guardado en: {output_path}")
        return True
    except Exception as e:
        print(f"Error al preparar el logo '{logo_path}': {e}")
        return False
