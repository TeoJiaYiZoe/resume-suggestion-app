import React, { useState } from 'react';
import axios from 'axios';
import './ResumeEditor.css';

const ResumeEditor = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [suggestedSolution, setSuggestedSolution] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('description', jobDescription);
    if (resumeFile) {
      formData.append('resume_file', resumeFile);
    }

    setLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/process_resume/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuggestedSolution(response.data.response);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1 className="welcome-header">Welcome to Resume Editor</h1>
    
      <div className='resume-editor-container'>
        <h3>Enter the Job Description:</h3>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Enter job description here"
          rows="4"
          cols="50"
        />
        <br />
        <div className="upload-section">
          <h3>Upload your resume:</h3>
          <label className="custom-file-upload">
            <input type="file" onChange={handleFileChange} />
            Choose File
          </label>
          {resumeFile && <span className="file-name">{resumeFile.name}</span>}
        </div>
        <br />
        <button onClick={handleSubmit}>Get Resume Suggestions</button>

        {loading && (
          <div className="loading-indicator">
            <span>Loading...</span>
          </div>
        )}

        {suggestedSolution && !loading && (
          <div className="suggested-solution">
            <h3>Suggested Solution:</h3>
            <p>{suggestedSolution}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeEditor;
