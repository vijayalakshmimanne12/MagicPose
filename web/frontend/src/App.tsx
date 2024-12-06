import { useState } from 'react'
import { 
  Container, 
  Paper, 
  Typography, 
  Button, 
  Box,
  CircularProgress,
  Grid
} from '@mui/material'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function App() {
  const [sourceImage, setSourceImage] = useState<File | null>(null)
  const [poseImage, setPoseImage] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    if (!sourceImage || !poseImage) {
      setError('Please select both source and pose images')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('source_image', sourceImage)
    formData.append('pose_image', poseImage)

    try {
      const response = await axios.post(`${API_URL}/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResults(response.data.output_images)
    } catch (err) {
      setError('An error occurred during processing')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Magic Dance Image Generator
        </Typography>

        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Source Image
          </Typography>
          <input
            accept="image/*"
            type="file"
            onChange={(e) => setSourceImage(e.target.files?.[0] || null)}
          />
        </Box>

        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Pose Image
          </Typography>
          <input
            accept="image/*"
            type="file"
            onChange={(e) => setPoseImage(e.target.files?.[0] || null)}
          />
        </Box>

        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}

        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={loading || !sourceImage || !poseImage}
        >
          {loading ? <CircularProgress size={24} /> : 'Generate'}
        </Button>

        {results.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Results
            </Typography>
            <Grid container spacing={2}>
              {results.map((imagePath, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <img
                    src={`${API_URL}/results/${imagePath}`}
                    alt={`Result ${index + 1}`}
                    style={{ width: '100%', height: 'auto' }}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Paper>
    </Container>
  )
}

export default App
