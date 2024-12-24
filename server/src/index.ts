import Router from "./routes/base.js";
import dotenv from "dotenv";
import cors from "cors";
import cookieParser from "cookie-parser";
import express from "express";
dotenv.config(); // Should print: your_password
const app = express();
app.use(
  cors({
    origin: ["http://localhost:5173"],
    credentials: true,
  })
);
app.use(cookieParser());
console.log("cors enabled");
const port = process.env.PORT || 3005;
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use("/claimendorsement", Router);
app.listen(port, () => {
  console.log(`Server running! port ${port}`);
});
