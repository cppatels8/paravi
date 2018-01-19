export const config = {
    canvas: {
        width: 1280,
        height: 720,
        frameRate: 25,
    },
    layers: [
        {
            actionType: 'play_video',
            name: 'examples/images/ICICI.mp4',
            duration: 20, // full
            // emit: { end: 'shadow_end' }
        },
        {
            actionType: 'text_graphics',
            text: 'Hi, Chandan Patel',
            font: '36px Tohama',
            color: '#555',
            animation: { effect: 'easeIn', duration: 5 },
            position: { end: { x: 520, y: 560 } },
            start_on: 7,
            end_on: 16
        }
    ]
}