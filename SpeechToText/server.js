require("dotenv").config();

const express = require("express");
const multer = require("multer");
const fs = require("fs");
const OpenAI = require("openai");

const app = express();

const upload = multer({
    dest: "uploads/"
});

const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

app.use(express.static("public"));

app.post("/transcribe", upload.single("audio"), async (req, res) => {
    try {
        const transcription = await client.audio.transcriptions.create({
            file: fs.createReadStream(req.file.path),
            model: "whisper-1"
        });

        fs.unlinkSync(req.file.path);

        res.json({
            text: transcription.text
        });

    } catch (error) {
        console.error("OpenAI Error:");
        console.error(error);

        if (error.response) {
            console.error(error.response.data);
        }

        res.status(500).json({
            text: "Error while transcribing."
        });
    }
});

app.listen(3000, () => {
    console.log("Server is running on http://localhost:3000");
});