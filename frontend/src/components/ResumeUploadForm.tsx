import React, { useState } from 'react';
import { toast } from 'sonner';
import { uploadResume } from '../services/resumeService';

export const ResumeUploadForm = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files ? event.target.files[0] : null;
    setFile(selectedFile);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      toast.error('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      await uploadResume(formData);
      toast.success('File uploaded successfully!');
    } catch (error: any) {
      toast.error(error.message || 'Failed to upload file.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={handleFileChange}
        aria-label="Upload Resume"
      />
      <button type="submit">Upload Resume</button>
    </form>
  );
};
