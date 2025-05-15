import React, { useEffect, useRef, useState } from 'react';
import { toast } from 'sonner';
// import CloudUploadIcon from '@mui/icons-material/CloudUpload';
// import DownloadingIcon from '@mui/icons-material/Downloading';
// import WarningIcon from '@mui/icons-material/Warning';
// import { Button } from '@mui/material';
// import { GridCheckCircleIcon } from '@mui/x-data-grid';
// import { sendFiles } from '@/src/actions/send-file';

type FileUploaderProps = {
  className?: string;
  size?: 'S' | 'M' | 'L';
  onFileUpload: (files: File[]) => void;
  fileUploadSuccess?: boolean;
  multiple?: boolean;
  accept?: string;
  maxFileSize?: number; // in megabytes
  extensions: string[];
};

const FileUploaderBox = ({
  onFileUpload,
  fileUploadSuccess = false,
  multiple = true,
  accept,
  // maxFileSize = Infinity,
  maxFileSize = 1,
  extensions = [],
}: FileUploaderProps) => {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [uploadSuccess, setUploadSuccess] =
    useState<boolean>(fileUploadSuccess);
  const [messageResponse, setMessageResponse] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const prepareFiles = (files: FileList) => {
    const maxFileSizeBytes = maxFileSize * 1024 * 1024; // Convert MB to bytes
    if (files) {
      const newSelectedFiles = Array.from(files);
      const tooLargeFiles = newSelectedFiles.filter(
        (file) => file.size > maxFileSizeBytes
      );
      if (tooLargeFiles.length > 0) {
        setError(
          `The file size must be less than or equal to ${maxFileSize} mb.`
        );
      } else {
        setError(null);
        setLoading(true);
        const readerPromises = newSelectedFiles.map(
          (file) =>
            new Promise<File>((resolve) => {
              const reader = new FileReader();
              reader.onloadend = () => {
                resolve(file);
              };
              reader.readAsDataURL(file);
            })
        );
        Promise.all(readerPromises).then((loadedFiles) => {
          setTimeout(() => {
            setSelectedFiles((prevSelectedFiles) => [
              ...prevSelectedFiles,
              ...loadedFiles,
            ]);
            setLoading(false);
            onFileUpload(loadedFiles);
          }, 1000);
        });
      }
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      prepareFiles(e.dataTransfer.files);
      onFileUpload(Array.from(e.dataTransfer.files));
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { files } = event.target;
    files && prepareFiles(files);
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleDeleteFile = (e: React.MouseEvent, index: number) => {
    e.preventDefault();
    e.stopPropagation();
    setSelectedFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  // const sendFiles = async () => {
  //   setLoading(true);
  //   try {
  //     const formData = new FormData();
  //     selectedFiles.forEach((file) => {
  //       formData.append("files", file);
  //     });

  //     const response = await fetch(
  //       "/api/excel",
  //       {
  //         method: "POST",
  //         body: formData,
  //       }
  //     );

  //     if (response.ok) {
  //       setUploadSuccess(true);
  //       setSelectedFiles([]);
  //       setError(null);

  //     } else {
  //       setError("Error uploading files");
  //     }
  //   } catch (error) {
  //     setError("Error uploading files");
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  const inputFile = (
    <input
      type="file"
      ref={fileInputRef}
      style={{ display: 'none' }}
      multiple={multiple}
      accept={accept}
      onChange={handleFileSelect}
    />
  );

  const uploadState = selectedFiles.length === 0 && (
    <div className="flex flex-col items-center justify-center">
      {/* <CloudUploadIcon /> */}
      <h2 className="text-lg font-bold">Cargar un archivo</h2>
      <p className="text-sm">Examinar archivos o arrastrar y soltar aquí</p>
      <p className="text-sm text-gray-500">
        El tamaño máximo de archivos es {maxFileSize} mb y solo{' '}
        {extensions.join(', ')} extensiones de archivos son permitidas
      </p>
    </div>
  );

  const successUpload = (
    <div className="flex flex-col items-center justify-center gap-2">
      {/* <GridCheckCircleIcon className="text-green-500" /> */}
      <p> Archivos Cargados </p>
      <p> {messageResponse} </p>
    </div>
  );

  const errorUpload = (
    <div className="flex">
      {/* <WarningIcon className="text-red-400" /> */}
      <h2 className="text-lg font-bold">¡No se puede cargar el archivo!</h2>
      <p className="text-red-400 text-sm">{error}</p>
      <button
        className="bg-gray-800 hover:bg-yellow-500 hover:text-black text-white font-bold py-2 px-4 rounded mt-5"
        onClick={() => handleButtonClick()}
      />
    </div>
  );

  const uploadingState = (
    <div className="bg-green-400 text-white p-4 rounded-lg">
      {/* <DownloadingIcon className="text-white" /> */}
      <p>Cargando...</p>
    </div>
  );

  const listFiles = selectedFiles.length > 0 && (
    <div className="flex flex-col items-center justify-center">
      {selectedFiles.map((file, index) => (
        <div key={index}>
          {file.name}
          <button onClick={(e) => handleDeleteFile(e, index)}>Eliminar</button>
        </div>
      ))}
    </div>
  );

  const listUploadedFiles = selectedFiles.length > 0 && (
    <>
      {/* <CloudUploadIcon className="text-green-500" /> */}
      <div className="flex flex-col items-center justify-center">
        <h2 className="text-lg font-bold">
          Su archivo está listo para ser cargado
        </h2>
        {listFiles}
      </div>
    </>
  );

  const handleSendFiles = async () => {
    const formData = new FormData();

    selectedFiles.forEach((file) => {
      formData.append('file', file);
    });
    setLoading(true);
    const response =  fetch(
      `https://api.transformer-service.tutti.addiis.co/orders/excel/upload`,
      {
        method: 'POST',
        body: formData,
      }
    ).then((response) => {
      setLoading(false);
      response.text().then((text) => {
        setMessageResponse(text);
        console.log(response);
        toast.success(text);
        setUploadSuccess(true);
        setSelectedFiles([]);
        setError(null);
      });
    });
  };
  const uploadButton =
    selectedFiles.length === 0 ? (
      <button
        className="bg-gray-800 hover:bg-yellow-500 hover:text-black text-white font-bold py-2 px-4 rounded mt-5"
        onClick={() => handleButtonClick()}
      >
        {' '}
        Inserta un archivo
      </button>
    ) : (
      <button
        className="bg-gray-800 hover:bg-yellow-500 hover:text-black text-white font-bold py-2 px-4 rounded mt-5"
        onClick={handleSendFiles}
      >
        Subir
      </button>
    );

  useEffect(() => {
    setUploadSuccess(fileUploadSuccess);
  }, [fileUploadSuccess]);

  return (
    <div
      className="flex flex-col items-center justify-center border-2 p-10 border-dashed border-gray-900"
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      {inputFile}

      {loading && uploadingState}
      {!loading && !uploadSuccess && !error && (
        <>
          {uploadState}
          {listUploadedFiles}
          {uploadButton}
        </>
      )}
      {uploadSuccess && (
        <>
          {successUpload}
          {listFiles}
        </>
      )}
      {error && <>{errorUpload}</>}
    </div>
  );
};

export type { FileUploaderProps };
export default FileUploaderBox;
