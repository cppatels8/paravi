import { getVideoDuration } from '../utils/Utils';

const EVENT_TYPES = { START: 0, END: 1 };


export function defineTimeline(config, frame_rate) {
    const events = {};
    // Read config and determine the videos, images and graphics to be overlayed in specified order in each frame
    let frames = [];

    subscribeEventAndSetDuration(config, events);
    updateEventTime(config, events);

    let videoTime = determineTotalVideoTime(config);
    let frameCount = parseInt(videoTime * frame_rate);

    let timeline = [];
    let frameDuration = 1 / frame_rate;
    for (let i = 0, t = 0; i < frameCount; i++ , t = i * frameDuration) {
        let m = [];
        config.layers.forEach(function (l) {
            if ((typeof l.start_on == 'number') && (typeof l.end_on == 'number') && t >= l.start_on && t < l.end_on) {
                m.push(l);
            }
        })

        timeline.push(m);
    }

    console.log("config :", config, videoTime, frameCount);
    return { timeline, frameCount, frameDuration, videoTime };
}


function subscribeEventAndSetDuration(config, events) {
    config.layers.forEach(function (layer, i) {
        // Check if action start time or event. If event, register to subscriptions
        // Determine the duration or event of action.

        if (!layer.start_on) {
            layer.start_on = 0;
        }
        else if (typeof layer.start_on === 'string') {
            subscribeEvent(events, layer.start_on, i, EVENT_TYPES.START);
        }

        if (!layer.end_on && (typeof layer.duration === 'number')) {
            // check duration
            if (layer.actionType == 'play_video' && layer.duration == -1) {
                layer.duration = getVideoDuration(layer.name);
            }
            if (typeof layer.start_on === 'number') {
                layer.end_on = layer.start_on + layer.duration;
            }
        }
        else if (typeof layer.end_on === 'string') {
            subscribeEvent(events, layer.end_on, i, EVENT_TYPES.END);
        }

    });
}

function updateEventTime(config, events) {
    config.layers.forEach(function (layer, i) {
        if (layer.emit) {
            for (let e in layer.emit) {
                if (e == 'end' && (typeof layer.end_on == 'number')) {
                    updateTimeOnEventOccurance(events, layer.emit[e], layer.end_on, config);
                } else if (e == 'start' && (typeof layer.start_on == 'number')) {
                    updateTimeOnEventOccurance(events, layer.emit[e], layer.start_on, config);
                }
            }
        }
    })

    config.layers.forEach(function (l) {
        if (!l.end_on && (typeof l.start_on == 'number') && (typeof l.duration == 'number')) {
            l.end_on = l.start_on + l.duration;
        }
    })
}




function determineTotalVideoTime(config) {
    let max_end = -1;
    config.layers.forEach(function (l) {
        if (typeof l.end_on == 'number' && l.end_on > max_end) {
            max_end = l.end_on;
        }
    })
    return max_end;
}



/////////////

function subscribeEvent(events, eventName, layerId, type) {
    if (!events[eventName]) {
        events[eventName] = { subscriptions: [], time: -1 };
    }
    events[eventName].subscriptions.push({ layer: layerId, type: type });
}

function updateTimeOnEventOccurance(events, eventName, time, config) {
    if (events[eventName]) {
        events[eventName].time = time;
        events[eventName].subscriptions.forEach(function (s, i) {
            let l = config.layers[s.layer];
            if (s.type === EVENT_TYPES.START) {
                config.layers[s.layer].start_on = time;
            } else if (s.type === EVENT_TYPES.END) {
                config.layers[s.layer].end_on = time;
            }
        })
        return true;
    }
    return false;
}

function getEventSubscriptions(events, eventName) {
    return events[eventName].subscriptions;
}
