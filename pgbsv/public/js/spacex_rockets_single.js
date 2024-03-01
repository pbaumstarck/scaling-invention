
/**
 * Timings:
 * 75: 277.235 s
 * 65: 256.935 s <-- Good.
 * 40: 206.249 s <-- Nice.
 * 10: 32.325 s
 */
let
    launches = getFalcon9FalconHeavyLaunches(),  // .slice(0, 5),
    launchIx = 0,
    falcon9RocketTable = null,
    orbitBarCharts = null,
    boosterStartFound = false,
    relativeBoosterChart = null,
    payloadMassChart = null,
    cumPayloadTons = 0,
    x = 1;

// var flightsBulletCounts = {};
// for (var i = 1; i <= 10; ++i) {
//     flightsBulletCounts[i] = 0;
// }

// If `increase`, promotes a booster from `boosterFlight - 1` to `boosterFlight`.
// If not `increase`, removes one booster from `boosterFlight`.
function updateFlightCountBullets(boosterFlight, increase) {
    // if (increase && flightsBulletCounts[boosterFlight - 1] > 0) {
    //     // Remove one bullet from last placeholder.
    //     flightsBulletCounts[boosterFlight - 1] -= 1;
    //     $(`#flights-bullets-${boosterFlight - 1}`).html('&bullet;'.repeat(flightsBulletCounts[boosterFlight - 1]) || '&nbsp;');
    // }

    // // Update latest placeholder.
    // flightsBulletCounts[boosterFlight] += increase ? 1 : -1;
    // $(`#flights-bullets-${boosterFlight}`).html('&bullet;'.repeat(flightsBulletCounts[boosterFlight]) || '&nbsp;');
}

function doLoop() {
    let url = new URL(document.location.href);
    let launchStopIx = url.searchParams.get('launchStopIx') && +url.searchParams.get('launchStopIx');
    let launchOffset = +url.searchParams.get('launchOffset') || 0;
    let boosterStart = url.searchParams.get('boosterStart') || '';
    let boosterOnly = url.searchParams.get('boosterOnly') || '';

    if (launchIx === launchStopIx) {
        return;
    }

    while (boosterOnly != null && boosterOnly.length > 0 && launchOffset + launchIx < launches.length &&
        launches[launchOffset + launchIx].booster != boosterOnly) {
        ++launchIx;
    }

    if (!boosterStartFound) {
        while (boosterStart != null && boosterStart.length > 0 && launchOffset + launchIx < launches.length &&
            launches[launchOffset + launchIx].booster != boosterStart) {
            ++launchIx;
        }
        boosterStartFound = true;
    }

    if (launchOffset + launchIx < launches.length) {
        var rockets = [launches[launchOffset + launchIx]];
        var retireDelay = 12.5 * TIME_MULTIPLE,
            postRetireDelay = 10 * TIME_MULTIPLE;
        if (rockets[0]._class == 'F9' && rockets[0].header.startsWith('FH')) {
            // Collate the three boosters of a Falcon Heavy.
            rockets.push(launches[launchOffset + launchIx + 1]);
            rockets.push(launches[launchOffset + launchIx + 2]);
            retireDelay = 30 * TIME_MULTIPLE;
            postRetireDelay = 30 * TIME_MULTIPLE;
        }

        var timeline = anime.timeline();
        let retiringClosures = rockets.map((r, ix) => falcon9RocketTable.handleRocketLaunch(r, timeline, ix));
        timeline.play();

        var relativeMove = rockets[0].is_retiring ? 1 - rockets[0].booster_flight : +1;
        if (rockets.length == 3) {
            var x = 1;
            if (rockets[1].is_retiring && (rockets[1].booster == 'B1023' || rockets[1].booster == 'B1025')) {
                // Have to take into account promoted FH Side cores, which accounted for two previous flights.
                relativeMove -= 2;
            } else if (rockets[1].is_retiring) {
                relativeMove += 1 - rockets[1].booster_flight;
            }
            if (rockets[2].is_retiring) {
                relativeMove += 1 - rockets[2].booster_flight;
            }
        }

        if (didRocketLaunch(rockets[0])) {
            // orbitBarCharts.addRocketLaunch(
            //     new Date(rockets[0].launch_datetime),
            //     rockets[0].orbit_class,
            //     OrbitTable.getPayloadMass(rockets[0].orbit_str, rockets[0].payload_mass_kg),
            // );
        }

        const launchDatetime = new Date(rockets[0].launch_datetime);
        let latestPointValue = relativeBoosterChart.recordRelativeMove(relativeMove, launchDatetime),
            rocketPayloadTons = 0.001 * OrbitTable.getPayloadMass(rockets[0]);
        cumPayloadTons += rocketPayloadTons;

        let finalClosure = () => {
            $('#booster-timeline-title .count').html(latestPointValue);
            $('#payload-timeline-title .count').html(cumPayloadTons.toFixed(0));
            relativeBoosterChart.render(() => setTimeout(doLoop, postRetireDelay));
            payloadMassChart.render(() => {});
        };
        payloadMassChart.recordRelativeMove(
            rocketPayloadTons,
            launchDatetime,
            // launchIx % 2 == 0 ? {
            //     rgb: '255, 128, 0',
            //     lineRgb: '255, 128, 0',
            //     useGradient: true,
            // } : {
            //     rgb: '128, 0, 255',
            //     lineRgb: '128, 0, 255',
            //     useGradient: true,
            // },
            {
                ...ORBIT_CLASSES_STRUCTS[rockets[0].orbit_class],
                useGradient: false,
            },
        );

        timeline.finished.then(() => {
            // relativeBoosterChart.render(() => {
            if (retiringClosures[0] == null && retiringClosures[1] == null && retiringClosures[2] == null) {
                finalClosure();
            } else {
                setTimeout(() => {
                    var retireTimeline = anime.timeline({
                        update: getAnimOnceClosure(finalClosure),
                    });
                    if (retiringClosures.length == 3) {
                        var x = 1;
                    }
                    // Play retiring closures in reverse, to move the side boosters before the core.
                    // for (var i = 0; i < retiringClosures.length; ++i) {
                    for (var i = retiringClosures.length - 1; i >= 0; --i) {
                        if (retiringClosures[i]) {
                            retiringClosures[i](retireTimeline);
                        }
                    }
                    retireTimeline.play();
                }, retireDelay);
            }
        });
        launchIx += rockets.length;
    } else {
        // Scoll out the screen once all animation is done.
        finishAnimation();
        // if (false) {
        //     var y = 0;
        //     setTimeout(() => {
        //         setInterval(() => window.scrollTo(0, y += 1), 10)
        //     }, 5000);
        // }
    }
}


class OrbitBarCharts {
    constructor(divId) {
        this._divId = divId;
        this._wrapper = $(`#${this._divId}`);

        this._startYear = 2010;
        const numYears = (new Date()).getFullYear() - this._startYear + 1;
        this._yearLabels = _.times(numYears, (y) => '' + (this._startYear + y));

        // Map from orbit classes to info about them.
        // this._orbitClassStructs = _.mapObject(ORBIT_CLASSES, (orbit) => {
        this._orbitChartData = _.object(ORBIT_CLASSES, _.map(ORBIT_CLASSES, (orbit) => _.times(numYears, () => 0)));
        const chartConfig = {
            type: 'bar',
            data: {
                labels: this._yearLabels,
                datasets: [
                    {
                        label: 'LEO, Sub-orbital',
                        data: this._orbitChartData['leo'],
                        borderColor: 'green',
                        backgroundColor: 'green',
                    },
                    {
                        label: 'SSO',
                        data: this._orbitChartData['sso'],
                        borderColor: 'blue',
                        backgroundColor: 'blue',
                    },
                    {
                        label: 'MEO, HEO',
                        data: this._orbitChartData['meo'],
                        borderColor: 'yellow',
                        backgroundColor: 'yellow',
                    },
                    {
                        label: 'GEO, GTO',
                        data: this._orbitChartData['geo'],
                        borderColor: 'red',
                        backgroundColor: 'red',
                    },
                    {
                        label: 'Lunar, Heliocentric, etc.',
                        data: this._orbitChartData['lunar'],
                        borderColor: 'purple',
                        backgroundColor: 'purple',
                    },
                ],
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'Total payload launched to orbit (tons)',
                        font: {
                            size: 16,
                        },
                    },
                },
                // interaction: {
                //     mode: 'nearest',
                //     axis: 'x',
                //     intersect: false
                // },
                // label: { display: false, },
                // plugins: {
                //     legend: {
                //         display: false
                //     },
                // },
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true,
                    },
                    // x: {
                    //     title: {
                    //         display: true,
                    //         text: 'Year'
                    //     }
                    // },
                }
            }
        };
        this._orbitChart = new Chart(document.getElementById('orbit-bar-chart'), chartConfig);

        // $(`#${orbit}-orbit-canvas`).css('height', 300);
        // $(`#${orbit}-orbit-canvas`).css('width', 300);

        // setTimeout(() => {
        //     orbitChart.data.datasets.forEach((dataset) => {
        //         dataset.data[dataset.data.length - 1] = 180000;
        //     });
        //     orbitChart.update();
        // }, 1000);
    }

    // handleRocketLaunch(rocket) {
    addRocketLaunch(launchDatetime, orbitClass, payloadKg) {
        const launchYear = launchDatetime.getFullYear();
            // orbitClass = OrbitTable.getOrbitClass(orbitStr);
        this._orbitChartData[orbitClass][launchYear - this._startYear] += 0.001 * payloadKg;
        this._orbitChart.update();
    }
}


function finishAnimation() {
    const pageDuration = +(new Date()) - PAGE_LOAD_DATETIME;
    if (FAST_MODE) {
        console.log(`Finished FAST_MODE page in ${pageDuration} ms`);
    } else {
        console.log(`Finished normal page in ${pageDuration} ms`);
        setTimeout(() => {
            document.location.href = `file:///Users/paul/Downloads/code/rockets/rocket_table_single.html?FAST_MODE=true&normal_duration=${pageDuration}`;
        }, 10000);
    }
}


$(document).ready(() => {
    const startDatetime = new Date((new Date(launches[0].launch_datetime)).getFullYear(), 0, 1, 0, 0, 0),
        endDatetime = new Date(+(new Date(launches[launches.length - 1].launch_datetime)) + 7 * 86400000);

    populateLegend(
        'total-launches-legend',
        [
            {
                label: 'Launch with Recovery',
                color: 'rgb(0, 255, 0)',
            },
            {
                label: 'Retiring Booster',
                color: 'rgb(255, 0, 0)',
            },
        ],
    );
    populateLegend(
        'total-payload-legend',
        // 'leo': {
        //     rgb: '128, 255, 128',
        //     lineRgb: '0, 128, 0',
        // },
        _.map(ORBIT_CLASSES_STRUCTS, (v) => {
            return {
                label: v.label,
                color: `rgb(${v.rgb})`,
            };
        }),
    );

    falcon9RocketTable = new Falcon9RocketTable('rocket-table', 'retiree-separator', true, 10);
    // TODO: Static function.
    // $('#timeline').css('height', 200).css('width', 840);
    relativeBoosterChart = new AreaTimelineChart(
        'booster-timeline',
        startDatetime,
        endDatetime,
        {
            useGradient: true,
            // width: 1670,
            // width: 840,
            xTicksBelow: true,
            yBounds: {
                yMin: 0,
                yMax: 5,
                yStep: 5,
            },
            colors: {
                positiveRgb: '128, 255, 128',
                positiveLineRgb: '0, 128, 0',
                negativeRgb: '255, 128, 128',
                negativeLineRgb: '255, 0, 0',
            },
        },
    );
    // orbitBarCharts = new OrbitBarCharts('orbit-container');
    payloadMassChart = new AreaTimelineChart(
        'payload-timeline',
        startDatetime,
        endDatetime,
        {
            useGradient: true,
            // width: 1670,
            // width: 840,
            xTicksBelow: true,
            yBounds: {
                yMin: 0,
                yMax: 10,
                yStep: 5,
            },
            // colors: {
            //     positiveRgb: '128, 255, 128',
            //     positiveLineRgb: '0, 128, 0',
            //     negativeRgb: '255, 128, 128',
            //     negativeLineRgb: '255, 0, 0',
            // },
        },
    );

    relativeBoosterChart.render(() => {
        // showLegendStartAnimation(() => {
        //     let url = new URL(document.location.href);
        //     let startDelay = url.searchParams.get('startDelay') && +url.searchParams.get('startDelay') || 1200;
        //     setTimeout(doLoop, startDelay);
        let url = new URL(document.location.href);
        let startDelay = url.searchParams.get('startDelay') && +url.searchParams.get('startDelay') || 0; // 1200;
        setTimeout(doLoop, startDelay);
    });

    payloadMassChart.render(() => {});
});
