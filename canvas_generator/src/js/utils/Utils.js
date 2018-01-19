import { exec, execSync } from 'child_process';
import fs from 'fs';


const VIDEO_DURATION_CMD = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ";
const VIDEO_FRAME_CMD = "ffmpeg -hide_banner -loglevel panic -i ";
const VIDEO_GENERATION_CMD = "cat tmp/*.jpg | ffmpeg -hide_banner -loglevel panic -f image2pipe -i - ";
/**
 * Determine the video duration in seconds
 */
export function getVideoDuration(videoFile) {
    let d = execSync(VIDEO_DURATION_CMD + videoFile).toString();
    // console.log(Number(d));
    return Number(d);
}

const TMP_VIDEO_FRAME_FILE = './temp.jpg';

export function getVideoFrame(videoFile, time) {
    if (fs.existsSync(TMP_VIDEO_FRAME_FILE)) {
        fs.unlinkSync(TMP_VIDEO_FRAME_FILE);
    }
    let cmd = VIDEO_FRAME_CMD + videoFile + " -ss " + time + " -vframes 1 " + TMP_VIDEO_FRAME_FILE;
    let d = execSync(cmd).toString();
    if (fs.existsSync(TMP_VIDEO_FRAME_FILE)) {
        let imageData = fs.readFileSync(TMP_VIDEO_FRAME_FILE);
        return imageData;
    } else {
        console.log(cmd + " :: " + d);
        return null;
    }
}

export function savePng(canvas, fileName) {

    fs.writeFileSync(fileName + '.jpg', canvas.toBuffer());
}


export function pad(num, size) {
    return ('000000000' + num).substr(-size);
}

export function createVideo(dir, fileName) {
    execSync(VIDEO_GENERATION_CMD + fileName);
}

export function rmDir(dir) {
    execSync('rm -rf ' + dir);
}

