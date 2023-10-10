const express = require("express");
const tf = require("@tensorflow/tfjs-node");
const multer = require("multer");
require("dotenv").config();
const path = require("path");
const fs = require("fs");
const bodyParser = require("body-parser");
const app = express();

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/"); // 업로드할 디렉토리를 지정합니다.
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname);
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + ext); // 파일 이름 설정 (고유한 이름)
  },
});

const upload = multer({ storage: storage });

// Body parser 설정
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const port = process.env.NODE_SERVER_PORT;
const modelURL = "https://teachablemachine.withgoogle.com/models/F9iHkNFrh/";

// 이미지 크기를 조정하고 Alpha 채널 제거하는 함수
async function preprocessImage(imagePath, targetWidth, targetHeight) {
  const imageBuffer = fs.readFileSync(imagePath);
  const imageTensor = tf.node.decodeImage(imageBuffer);

  // 이미지 크기 조정
  const resizedImageTensor = tf.image.resizeBilinear(imageTensor, [
    targetHeight,
    targetWidth,
  ]);

  // Alpha 채널 제거 (RGBA에서 RGB로 변환)
  const rgbImageTensor = tf.slice(resizedImageTensor, [0, 0, 0], [-1, -1, 3]);

  // 이미지를 [0, 1] 범위로 정규화
  const normalizedImageTensor = rgbImageTensor.div(255.0);

  return normalizedImageTensor;
}

async function classifyImage(imagePath) {
  // Teachable Machine 모델 로드
  const modelPath = "model.json";
  const model = await tf.loadLayersModel(`file://${modelPath}`);

  // 이미지 크기 조정 및 Alpha 채널 제거
  const targetWidth = 224;
  const targetHeight = 224;
  const preprocessedImageTensor = await preprocessImage(
    imagePath,
    targetWidth,
    targetHeight
  );

  // 이미지를 4차원으로 reshape
  const reshapedImageTensor = preprocessedImageTensor.reshape([
    1,
    targetHeight,
    targetWidth,
    3,
  ]);

  // 모델에 이미지를 입력으로 주고 예측 수행
  const predictions = model.predict(reshapedImageTensor);

  // 예측 결과를 JSON으로 변환
  const predictionsArray = Array.from(predictions.dataSync());

  return predictionsArray;
}

app.post("/", upload.single("image"), async (req, res) => {
  const uploadedFile = req.file;

  if (uploadedFile.mimetype === "image/png") {
    const destinationPath = "uploads/" + uploadedFile.filename;

    fs.rename(uploadedFile.path, destinationPath, async (err) => {
      if (err) {
        console.error(err);
        res.status(500).send("파일 저장 중에 오류가 발생했습니다.");
      } else {
        try {
          console.log(uploadedFile.filename);
          const predictions = await classifyImage(destinationPath);
          res.json(predictions);
        } catch (err) {
          console.error("이미지 분류 오류:", err);
          res.status(500).json({ rtnMsg: "이미지 분류 오류" });
        }
      }
    });
  } else {
    fs.unlink(uploadedFile.path, (err) => {
      if (err) {
        console.error(err);
      }
      res.status(400).send("PNG 파일만 업로드할 수 있습니다.");
    });
  }
});

app.listen(port, () => console.log(port));
