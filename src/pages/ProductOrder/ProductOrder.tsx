import FileUploaderBox from "./components/DragAndDrop";

const ProductOrder = () => {
  return (
    <>
      <h2 className="text-3xl font-bold">Orden Producto</h2>
      <FileUploaderBox
        extensions={['.xlsx', '.xls']}
        onFileUpload={function (files: File[]): void {}}
      ></FileUploaderBox>
    </>
  );
};

export default ProductOrder;
