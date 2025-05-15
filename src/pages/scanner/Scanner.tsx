import React, { useEffect, useState } from "react";
import Quagga from "quagga"; // Ensure QuaggaJS is installed via npm

interface Props {
  onCodeScanned?: (scannedCode: string) => void;
  onStopScanning?: () => void; // Nueva prop para detener el escaneo
}

const Scanner = ({ onCodeScanned, onStopScanning }: Props) => {
  const [scannedCode, setScannedCode] = useState("");
  const [isScanning, setIsScanning] = useState(true);

  const startScanner = () => {
    Quagga.init(
      {
        inputStream: {
          name: "Live",
          type: "LiveStream",
          target: document.querySelector("#interactive"),
        },
        decoder: {
          readers: ["code_128_reader", "ean_reader", "ean_8_reader"],
        },
      },
      (err) => {
        if (err) {
          console.error(err);
          return;
        }
        Quagga.start();
      }
    );

    Quagga.onDetected((result) => {
      const code = result.codeResult.code;
      setScannedCode(code);
      if (onCodeScanned) {
        onCodeScanned(code);
      }
    });
  };

  const stopScanner = () => {
    Quagga.stop();
    setIsScanning(false);
    if (onStopScanning) {
      onStopScanning(); // Llamar a la función proporcionada por el componente padre
    }
  };

  useEffect(() => {
    if (isScanning) {
      startScanner();
    }

    return () => {
      Quagga.stop();
    };
  }, [isScanning]);

  if (!isScanning) {
    return null; // No renderizar nada si no está escaneando
  }

  return (
    <div id="scanner-container">
      <div
        id="interactive"
        className="viewport"
        style={{ width: "100%", maxWidth: "100%", margin: "20px auto" }}
      >
        {/* Live video feed from the scanner will be displayed here */}
      </div>
      <button
        onClick={stopScanner}
        style={{
          marginTop: "10px",
          padding: "10px 20px",
          backgroundColor: "red",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        Detener Scanner
      </button>
      <p
        id="barcode-result"
        style={{ marginTop: "20px", fontSize: "18px", fontWeight: "bold" }}
      >
        {scannedCode
          ? `Scanned Barcode: ${scannedCode}`
          : "Acá tu codigo de barras"}
      </p>
    </div>
  );
};

export default Scanner;
