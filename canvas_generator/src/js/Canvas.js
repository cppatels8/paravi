import fs from 'fs';
import { createCanvas, loadImage, Image } from 'canvas'
import { JSDOM } from 'jsdom';

import { config } from './config/JoinVideos.example';
import { defineTimeline } from './timeline/Timeline';
import { getVideoFrame, savePng, pad, rmDir, createVideo } from './utils/Utils';


const FRAME_RATE = 24;
const IMG_TMP_DIR = 'tmp';
const IMG_PREFIX = 'tmp/Img_';


// Create video


// read configuration, to determine the videos to be played and for how much time. Also what visual templates to be applied over it.
/**
 * Assuming 2 videos to be played, one after another and welcome text over each video, with animation to be provided.
 */
function main() {
    cleanup();

    let timelineConfig = defineTimeline(config, FRAME_RATE);
    startRecording(timelineConfig);

    let videoFile = (process.env.OUTPUT) ? process.env.OUTPUT : 'video.mp4';
    createVideo(IMG_TMP_DIR, videoFile);
}

function cleanup() {
    if (fs.existsSync(IMG_TMP_DIR)) {
        rmDir(IMG_TMP_DIR);
        // fs.rmdirSync(IMG_TMP_DIR);

    }
    fs.mkdirSync(IMG_TMP_DIR);
}



function startRecording(timelineConfig) {
    const canvas = createCanvas(600, 400)
    const ctx = canvas.getContext('2d')

    timelineConfig.timeline.forEach(function (t, i) {
        let time = timelineConfig.frameDuration * i;

        // if (i > 0) { return; }

        // clear the canvas
        ctx.clearRect(0, 0, 600, 400);

        // iterate through each action in that timeframe
        t.forEach(function (a, j) {
            if (a.actionType == 'play_video') {
                saveVideoFrame(a.name, time - a.start_on, canvas, ctx);
            }
            return;
        })

        // save the output in a jpg file
        savePng(canvas, IMG_PREFIX + pad(i, 4));
    })

    // Initiate frame by frame rendering
}

function renderFrame(config) {
    // clear the canvas

    // loop through the array of renderings to be applied in specified order
    // And keeping drawing the image on the canvas

    // Save the image to the output

}

function saveVideoFrame(videoFile, time, canvas, ctx) {
    let imageData = getVideoFrame(videoFile, time);
    if (imageData) {
        // console.log("***************time :", time, imageData.buffer.byteLength);
        let i = new Image;
        i.src = imageData;
        ctx.drawImage(i, 0, 0);
    }

    ctx.font = '30px Impact'
    ctx.fillStyle = 'yellow';
    // ctx.rotate(0.1)
    ctx.fillText('Awesome!', 50 + (5 * time), 100 + (5 * time));
    // ctx.fillStyle = '#DD9';
    // ctx.fillRect(0, 0, 600, 400);
}

function getImage(imageFile, renderingConfig) {

}

function getAnimationFrame(animationType, config, time) {

}


// Start the processing
main();