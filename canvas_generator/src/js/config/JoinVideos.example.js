export const config = {
    layers: [
        {
            actionType: 'play_video',
            name: 'examples/images/shadow.mp4',
            duration: -1, // full
            emit: { end: 'shadow_end' }
        },
        {
            start_on: 'shadow_end',
            actionType: 'play_video',
            name: 'examples/images/video2.mp4',
            duration: -1, // full
            emit: { end: 'video2_end' }
        },
        {
            actionType: 'text_graphics',
            text: 'Playing shadow.mp4 :)',
            background: 'yellow',
            color: 'red',
            zoom: { scale: 2, duration: 2, duration_unit: 'sec' },
            end_on: 'shadow_end'
        },
        {
            start_on: 'shadow_end',
            actionType: 'text_graphics',
            text: 'Playing Video2.mp4 now :)',
            background: 'red',
            color: 'yellow',
            zoom: { scale: 2, duration: 2, duration_unit: 'sec' }
        }
    ]
}