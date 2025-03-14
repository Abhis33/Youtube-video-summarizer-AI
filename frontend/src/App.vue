<template>
<div id="app">
  <div class="container">
    <header>
      <h1>YouTube Video Summarizer</h1>
      <p class="tagline">Get concise summaries of any YouTube video</p>
    </header>

    <form @submit.prevent="submitUrl" class="search-form">
      <div class="input-group">
        <input type="text" v-model="youtubeUrl" placeholder="Enter YouTube URL" required class="url-input" />
        <button type="submit" class="btn-submit">
          <span v-if="loading">Processing...</span>
          <span v-else>Summarize</span>
        </button>
      </div>
    </form>

    <div v-if="loading" class="loading-indicator">
      <div class="spinner"></div>
      <p>Fetching and analyzing video content...</p>
    </div>

    <div v-if="summary" class="summary-container">
      <h2>Summary</h2>
      <div class="summary-content">
        {{ summary }}
      </div>
    </div>

    <div v-if="error" class="error-container">
      <h2>Error</h2>
      <div class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      youtubeUrl: '',
      summary: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async submitUrl() {
      this.summary = ''
      this.error = ''
      this.loading = true

      try {
        const response = await axios.post('http://localhost:5000/summarize', {
          url: this.youtubeUrl
        });
        if (response.data.summary) {
          this.summary = response.data.summary;
        } else if (response.data.error) {
          this.error = response.data.error;
        }
      } catch (err) {
        console.error('Error:', err);
        this.error = err.response ? .data ? .error || 'An error occurred while summarizing.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style>
/* General styles */
:root {
  --primary-color: #4a6cf7;
  --secondary-color: #f5f5f5;
  --text-color: #333;
  --error-color: #e74c3c;
  --border-radius: 8px;
  --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f9f9f9;
  color: var(--text-color);
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

#app {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.container {
  max-width: 800px;
  width: 100%;
}

/* Header styles */
header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

h1 {
  color: var(--primary-color);
  margin-bottom: 10px;
  font-size: 2.5rem;
}

.tagline {
  color: #777;
  font-size: 1.1rem;
  margin-top: 0;
}

/* Form styles */
.search-form {
  margin-bottom: 30px;
}

.input-group {
  display: flex;
  gap: 10px;
}

.url-input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.url-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
}

.btn-submit {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-submit:hover {
  background-color: #3a5cd8;
}

.btn-submit:active {
  transform: translateY(1px);
}

/* Loading indicator */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Summary container */
.summary-container,
.error-container {
  background-color: white;
  border-radius: var(--border-radius);
  padding: 25px;
  margin-top: 20px;
  box-shadow: var(--box-shadow);
}

.summary-container h2,
.error-container h2 {
  margin-top: 0;
  color: var(--primary-color);
  font-size: 1.5rem;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.summary-content {
  line-height: 1.7;
  white-space: pre-line;
}

/* Error message */
.error-container {
  border-left: 4px solid var(--error-color);
}

.error-container h2 {
  color: var(--error-color);
}

.error-message {
  color: var(--error-color);
  font-weight: 500;
}

/* Responsive design */
@media (max-width: 600px) {
  .input-group {
    flex-direction: column;
  }

  .btn-submit {
    width: 100%;
  }
}
</style>
