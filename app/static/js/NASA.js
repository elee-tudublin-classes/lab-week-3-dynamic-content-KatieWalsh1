require('dotenv').config();
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.use(express.static('public'));

// Route to fetch NASA APOD data
app.get('/apod', async (req, res) => {
    try {
        const response = await axios.get(`${process.env.NASA_API_URL}`, {
            params: {
                api_key: process.env.NASA_API_KEY
            }
        });
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch APOD data' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
