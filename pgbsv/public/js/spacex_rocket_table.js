
let
    ENTRANCE_DURATION_MS = FAST_MODE ? 20 : 200,
    // ENTRANCE_DURATION_MS = 1,
    // BOOSTER_TABLE_TOP = 48,
    // BOOSTER_TABLE_TOP = /*TIMELINE_HEIGHT +*/ 52,  // Were missing four pixels.
    BOOSTER_TABLE_TOP = /*TIMELINE_HEIGHT +*/ 0,  // Were missing four pixels.
    ORBIT_PAYLOAD_HEIGHT = 11,
    BOOSTER_ROW_HEIGHT = 58 + ORBIT_PAYLOAD_HEIGHT,
    BOOSTER_ROW_ADDITIONAL_HEIGHT = 57 + ORBIT_PAYLOAD_HEIGHT,
    RETIREE_SEPARATOR_TOP_OFFSET = 33 + ORBIT_PAYLOAD_HEIGHT,
    // BOOSTER_LAUNCH_COLUMNS = 10,
    // BOOSTER_LAUNCH_COLUMNS = 5,
    FADE_IN_START_STYLE = `opacity: 0; ${FAST_MODE ? '' : ' animation-name: unblur; animation-duration: 0.5s;'}`;


class RocketTable {
    constructor(rocketTableId, retireeId, animateFlightBullets, boosterLaunchColumns) {
        // Div to contain things.
        this.rocketTableId = rocketTableId;
        this.retireeId = retireeId;
        this.boosterLaunchColumns = boosterLaunchColumns;
        // TODO: More HTML parameters.
        // List of launches to render.
        // this.launches = launches;

        // Whether to animate the flight bullet counters (single-page only).
        this.animateFlightBullets = animateFlightBullets;

        // Whether we are showing the retiree separator.
        this.showRetireeSeparator = false;
        // { position: Number, height: Number }
        this.boosterData = {};

        // Map with keys of booster IDs and values of lists of launch objects.
        this.boosterToLaunches = {};

        // Booster given a crown to represent life leader.
        // this.crownBooster = null;
    }

    // If `preceding`, shifts all boosters before `booster` down one.
    // If not `preceding`, shifts all boosters after `booster` up one.
    // Returns the total height of qualifying boosters.
    shiftBoosters(timeline, booster, preceding, opt_boosterPosition, opt_closure) {
        // Need to re-sort everyone.
        let boosterOldPos = this.boosterData[booster].position,
            boosterOldHeight = this.boosterData[booster].height,
            boosterPosition = opt_boosterPosition || 0;
        var movingBoosterHeight = 0,
            movingBoosterKeys = [];
        for (var key in this.boosterData) {
            if (preceding && this.boosterData[key].position < boosterOldPos && this.boosterData[key].position >= boosterPosition ||
                !preceding && this.boosterData[key].position > boosterOldPos) {
                // Need to move this booster.
                this.boosterData[key].position += preceding ? 1 : -1;
                movingBoosterHeight += this.boosterData[key].height;
                movingBoosterKeys.push(`#${key}`);
            }
        }

        if (preceding) {
            // Move this booster to its desired position.
            this.boosterData[booster].position = boosterPosition;
        } else {
            // Remove this boosters from the list.
            // TODO: Make position -1 or something to kick it off the list.
            delete this.boosterData[booster];
        }

        if (opt_closure) {
            opt_closure(movingBoosterHeight);
        }
        if (movingBoosterKeys.length) {
            timeline.add({
                targets: movingBoosterKeys.join(', '),
                duration: ENTRANCE_DURATION_MS,
                easing: 'linear',
                translateY: (preceding ? '+=' : '-=') + ` ${boosterOldHeight}px`,
            // }, 0);
            });
        }
        return movingBoosterHeight;
    }

    _createBoosterRow(rocket, boosterTop) {
        throw 'Not Implemented'
    }

    _addNewBooster(rocket, timeline, boosterPosition) {
        let { booster,
              booster_version,
              booster_version_class,
        } = rocket;
        let boosterRowHeight = BOOSTER_ROW_HEIGHT,
            boosterRow = this._createBoosterRow(rocket, BOOSTER_TABLE_TOP + boosterPosition * BOOSTER_ROW_HEIGHT);
        $(`#${this.rocketTableId}`).append(boosterRow);
        boosterRow.on('animationend', () => $(this).removeClass('unblur-animation'));

        var movingBoosterKeys = [];
        for (var key in this.boosterData) {
            if (this.boosterData[key].position >= boosterPosition) {
                this.boosterData[key].position += 1;
                movingBoosterKeys.push(`#${key}`);
            }
        }
        this.boosterData[booster] = {
            height: boosterRowHeight,
            position: boosterPosition,
        };

        // And shift all other boosters down a row.
        timeline.add({
            targets: `${movingBoosterKeys.length ? movingBoosterKeys.join(', ') + ', ' : ''} #${this.rocketTableId} .booster-row.retired, #${this.retireeId}`,
            duration: ENTRANCE_DURATION_MS,
            easing: 'linear',
            translateY: `+= ${boosterRowHeight}px`,
        });
        // Fade the new booster in.
        timeline.add({
            targets: `#${booster}`,
            duration: ENTRANCE_DURATION_MS,
            easing: 'linear',
            opacity: 1,
        });
    }

    // Shifts an existing booster into proper position to add the latest launch to it.
    _shiftExistingBooster(rocket, timeline, willBoosterRowWrap, opt_boosterPosition) {
        let {
            booster,
            booster_version_class,
            booster_version,
            _operator,
        } = rocket;
        if (willBoosterRowWrap) {
            // Shift all retired things and succeeding bosoter down by the added height.
            this.boosterData[booster].height += BOOSTER_ROW_ADDITIONAL_HEIGHT;

            var succeedingKeys = [];
            for (var key in this.boosterData) {
                if (this.boosterData[key].position > this.boosterData[booster].position) {
                    succeedingKeys.push(`#${key}`)
                }
            }

            var targets = `#${this.rocketTableId} .booster-row.retired, #${this.retireeId}`;
            if (succeedingKeys.length) {
                targets += ', ' + succeedingKeys.join(', ')
            }
            timeline.add({
                targets: targets,
                duration: ENTRANCE_DURATION_MS,
                easing: 'linear',
                translateY: `+= ${BOOSTER_ROW_ADDITIONAL_HEIGHT}px`,
            });
        }

        // Shift preceding boosters down one, and shift the just flown booster to the top.
        let precedingBoosterHeight = this.shiftBoosters(timeline, booster, true, opt_boosterPosition);
        timeline.add({
            targets: `#${booster}`,
            duration: ENTRANCE_DURATION_MS,
            translateY: `-= ${precedingBoosterHeight}px`,
            easing: 'easeOutQuad',
            update: getAnimOnceClosure(() => {
                // Assert the booster has the correct current version.
                // if (_operator == 'SpaceX' && booster_version == 'FH Side') {
                $(`#${booster} .booster-version`)
                    .removeClass()
                    .addClass(`booster-version ${booster_version_class}`)
                    .text(booster_version);
                console.log(`Shoulda promoted ${booster}`);
            })
        });
        // Blur out the booster name and unblur-animate it.
        // TODO: Not working!
        // $(`#${booster} .booster-name`)
        //     .addClass('unblur-animation')
        //     .on('animationend', () => { console.log('Anim end'); $(this).removeClass('unblur-animation'); });
    }

    _createBoosterEvent(rocket, isNewBooster, willBoosterRowWrap) {
        throw 'Not Implemented'
    }

    _addBoosterLaunch(rocket, timeline, isNewBooster, willBoosterRowWrap) {
        let {
            booster,
        } = rocket,
            launchId = getLaunchId(rocket, this.launchId);

        $(`#${booster}`).append(this._createBoosterEvent(rocket, isNewBooster, willBoosterRowWrap));
        if (!isNewBooster) {
            // Fade the new launch in by itself,
            timeline.add({
                targets: `#${launchId}`,
                duration: ENTRANCE_DURATION_MS,
                easing: 'linear',
                opacity: 1,
            });
        }
    }

    _createRetiringClosure(rocket) {
        let {
            booster,
            booster_flight,
        } = rocket;

        return (retireTimeline) => {
            let oldBoosterHeight = this.boosterData[booster].height;
            $(`#${booster}`).removeClass('active').addClass('retired');

            // Shift succeeding boosters up one, and shift the just flown booster to the top of the retiree list.
            this.shiftBoosters(retireTimeline, booster, false, undefined, (succeedingBoostersHeight) => {
                retireTimeline.add({
                    targets: `#${booster}`,
                    duration: ENTRANCE_DURATION_MS,
                    // translateY: `+= ${succeedingBoosters * BOOSTER_ROW_HEIGHT + RETIREE_SEPARATOR_TOP_OFFSET}px`,
                    translateY: `+= ${succeedingBoostersHeight + RETIREE_SEPARATOR_TOP_OFFSET}px`,
                    easing: 'easeOutQuad',
                });
            });
            if (this.showRetireeSeparator) {
                retireTimeline.add({
                    targets: `#${this.retireeId}`,
                    duration: ENTRANCE_DURATION_MS,
                    easing: 'linear',
                    translateY: `-= ${oldBoosterHeight}px`,
                });
            } else {
                this.showRetireeSeparator = true;
                retireTimeline.add({
                    targets: `#${this.retireeId}`,
                    duration: ENTRANCE_DURATION_MS,
                    easing: 'linear',
                    opacity: 1,
                });
            }

            if (this.animateFlightBullets) {
                updateFlightCountBullets(booster_flight, false);
            }
        };
    }

    handleRocketLaunch(rocket, timeline, opt_boosterPosition) {
        let { booster,
              header,
              launch_datetime,
              launch_outcome_class,
              booster_version,
              payload_str,
              booster_landing_str,
              booster_landing_class,
              booster_version_class,
              booster_flight,
              booster_landing_method,
              is_retiring } = rocket;
        let isNewBooster = !(booster in this.boosterData);
        console.log(`Handling ${booster} - ${payload_str}` + (isNewBooster ? ' (new)' : ''));
        if (isNewBooster) {
            this.boosterToLaunches[booster] = [rocket];
        } else {
            this.boosterToLaunches[booster].push(rocket);
        }
        let boosterLaunches = this.boosterToLaunches[booster],
            willBoosterRowWrap = boosterLaunches.length >= this.boosterLaunchColumns && boosterLaunches.length % this.boosterLaunchColumns == 1,
            boosterPosition = opt_boosterPosition || 0;

        if (isNewBooster) {
            this._addNewBooster(rocket, timeline, boosterPosition);
            // if (willBoosterRowWrap) {
            //     throw 'This should not happen';
            // }
        } else {
            this._shiftExistingBooster(rocket, timeline, willBoosterRowWrap, opt_boosterPosition);
        }

        this._addBoosterLaunch(rocket, timeline, isNewBooster, willBoosterRowWrap);

        if (this.animateFlightBullets) {
           updateFlightCountBullets(booster_flight, true);
        }

        // Retire the booster if this was its last flight.
        if (is_retiring) {
            return this._createRetiringClosure(rocket);
        } else {
            return null;
        }
    }
}

class Falcon9RocketTable extends RocketTable {
    _createBoosterRow(rocket, boosterTop) {
        let {
            booster,
            booster_version,
            booster_version_class,
        } = rocket;
        return $(
            `<div id="${booster}" class="booster-row active ${FAST_MODE ? '' : ' unblur-animation'}" style="opacity: 0; top: ${boosterTop}px;">` +
                `<div class="booster-name th-cell cell-width">` +
                    `<span class="booster-version ${booster_version_class}">${booster_version}</span>` +
                    `<span class="block-number">${booster}</span>` +
                    `<span class="block-crown" style="display: none;">👑</span>` +
                `</div>` +
            `</div>`
        );
    }

    _createBoosterEvent(rocket, isNewBooster, willBoosterRowWrap) {
        let {
            booster,
            booster_landing_class,
            booster_landing_method,
            launch_datetime,
            launch_outcome_class,
            orbit_str,
            payload_mass_kg,
            payload_mass_str,
            payload_str,
            is_crewed,
        } = rocket,
            launchId = getLaunchId(rocket, this.launchId),
            boosterLaunches = this.boosterToLaunches[booster],
            payloadDisplay = payload_mass_kg != null ? numberWithCommas(payload_mass_kg) + ' kg' : payload_mass_str;

        var daysSinceLastLaunch = -1;
        if (!isNewBooster) {
            daysSinceLastLaunch = Math.round(
                (
                    new Date(boosterLaunches[boosterLaunches.length - 1].launch_datetime.substring(0, 10)) -
                    new Date(boosterLaunches[boosterLaunches.length - 2].launch_datetime.substring(0, 10))
                ) / 86400000.0
            );
        }

        const payloadStrDisplay = (is_crewed ? ASTRONAUT_EMOJI : '') + payload_str;
        return $(
            (willBoosterRowWrap ? '<br>' : '') +  // Wrap every n'th launch.
            `<div id="${launchId}" class="booster-launch-wrapper ${willBoosterRowWrap ? ' booster-row-wrap' : ''}" ${isNewBooster ? '' : ` style="${FADE_IN_START_STYLE}"`}>` +
                (isNewBooster ? '' : `<span class="launch-interim">${daysSinceLastLaunch}<br>&rarr;<br>days</span>`) +
                `<div class="booster-launch ${payload_str.startsWith('Starlink') ? 'megaconstellation' : ''} td-cell cell-width">` +
                    `<div class="launch-date cell-width">${launch_datetime.substring(0, 10)}</div>` +
                    `<div class="launch outcome cell-width ${launch_outcome_class}">${payloadStrDisplay}</div>` +
                    `<div class="payload outcome cell-width ${launch_outcome_class}">` +
                        `${orbit_str} - ${payloadDisplay}` +
                    `</div>` +
                    `<div class="landing outcome cell-width ${booster_landing_class}">${booster_landing_method}</div>` +
                `</div>` +
            `</div>`,
        );
    }
}

class UlaRocketTable extends RocketTable {
    _createBoosterRow(rocket, boosterTop) {
        let {
            booster,
            _class,
            booster_version,
            booster_version_class,
        } = rocket;
        return $(
            `<div id="${booster}" class="booster-row active ${FAST_MODE ? '' : ' unblur-animation'}" style="opacity: 0; top: ${boosterTop}px;">` +
                `<div class="booster-name ${_class.toLowerCase()} th-cell cell-width">` +
                    `<span class="booster-version ${booster_version_class}">${booster_version}</span>` +
                    `<span class="block-number">${booster}</span>` +
                    `<span class="block-crown" style="display: none;">👑</span>` +
                `</div>` +
            `</div>`
        );
    }

    _createBoosterEvent(rocket, isNewBooster, willBoosterRowWrap) {
        let {
            booster,
            booster_landing_class,
            booster_landing_method,
            launch_datetime,
            launch_outcome_class,
            orbit_str,
            payload_mass_kg,
            payload_mass_str,
            payload_str,
        } = rocket,
            launchId = getLaunchId(rocket, this.launchId),
            boosterLaunches = this.boosterToLaunches[booster],
            payloadDisplay = payload_mass_kg != null ? numberWithCommas(payload_mass_kg) + ' kg' : payload_mass_str;

        var daysSinceLastLaunch = -1;
        if (!isNewBooster) {
            daysSinceLastLaunch = Math.round(
                (
                    new Date(boosterLaunches[boosterLaunches.length - 1].launch_datetime.substring(0, 10)) -
                    new Date(boosterLaunches[boosterLaunches.length - 2].launch_datetime.substring(0, 10))
                ) / 86400000.0
            );
        }
        return $(
            `<div id="${launchId}" class="booster-launch-wrapper">` +
                `<div class="booster-launch ${payload_str.startsWith('OneWeb') ? 'megaconstellation' : ''} td-cell cell-width">` +
                    `<div class="launch-date cell-width">${launch_datetime.substring(0, 10)}</div>` +
                    `<div class="launch outcome cell-width ${launch_outcome_class}">${payload_str}</div>` +
                    `<div class="payload outcome cell-width ${launch_outcome_class}">` +
                        `${orbit_str} - ${payloadDisplay}` +
                    `</div>` +
                    // `<div class="landing outcome cell-width no-attempt">N/A</div>` +
                    `<div class="landing outcome cell-width ${booster_landing_class}">${booster_landing_method}</div>` +
                `</div>` +
            `</div>`,
        );
    }
}

class StarshipTable extends RocketTable {
    _createBoosterRow(rocket, boosterTop) {
        let {
            booster,
            vehicle,
            booster_version,
            booster_version_class,
        } = rocket;
        return $(
            `<div id="${booster}" class="booster-row active ${FAST_MODE ? '' : ' unblur-animation'}" style="opacity: 0; top: ${boosterTop}px;">` +
                `<div class="booster-name th-cell cell-width">` +
                    // `<span class="booster-version ${booster_version_class}">${booster_version}</span>` +
                    `<span class="block-number">${vehicle}</span>` +
                    `<span class="block-crown" style="display: none;">👑</span>` +
                `</div>` +
            `</div>`
        );
    }

    _createBoosterEvent(rocket, isNewBooster, willBoosterRowWrap) {
        let {
            booster,
            booster_landing_class,
            booster_landing_method,
            launch_datetime,
            launch_outcome_class,
            type,
            event,
            outcome,
            outcome_class,
            height,
            landing,
            landing_class,
        } = rocket,
            launchId = getLaunchId(rocket, this.launchId),
            boosterLaunches = this.boosterToLaunches[booster];

        var daysSinceLastLaunch = -1;
        if (!isNewBooster) {
            daysSinceLastLaunch = Math.round(
                (
                    new Date(boosterLaunches[boosterLaunches.length - 1].launch_datetime.substring(0, 10)) -
                    new Date(boosterLaunches[boosterLaunches.length - 2].launch_datetime.substring(0, 10))
                ) / 86400000.0
            );
        }

        var body = `<div class="double-line-item-event outcome cell-width">?<br>?</div>`;;
        if (type == 'Construction') {
            if (event == 'Begins') {
                body = `<div class="double-line-item-event construction outcome cell-width">Construction<br>started</div>`;
            } else if (event == 'Completed') {
                body = `<div class="double-line-item-event construction outcome cell-width">Construction<br>completed</div>`;
            } else if (event == 'Halted') {
                body = `<div class="double-line-item-event construction outcome retired cell-width">Construction<br>halted</div>`;
            }
        } else if (type == 'Retired') {
            body = `<div class="single-line-item-event retired outcome cell-width">Retired</div>`;
        } else if (type == 'Testing') {
            if (event == 'Hop') {
                let landingEmoji = (
                        landing == 'Partial success' ? TROPHY_EMOJI + EXPLOSION_EMOJI :
                            (landing == 'Success' ? TROPHY_EMOJI : EXPLOSION_EMOJI)
                );
                body = (
                    `<div class="launch outcome ${outcome_class} cell-width">${height} ${event} ${ROCKET_EMOJI}</div>` +
                    `<div class="landing outcome ${landing_class} cell-width">${landing} ${landingEmoji}</div>`
                );
                // Flight  Tethered hop    Success     0.2 m
            // } else if (event == 'Tethered hop') {
            //     body = (
            //         `<div class="launch outcome ${outcome_class} cell-width">${height} ${event} ${FLAME_EMOJI}</div>` +
            //         `<div class="landing outcome ${landing_class} cell-width">${landing}</div>`
            //     );
            } else {  // if (event == 'Pressure test' || event == 'Water pressure test') {
                var copy = `${event}`;
                // var emoji = '&nbsp;';
                if (event == 'Water pressure test') {
                    copy += '&nbsp' + DROPLETS_EMOJI;
                } else if (event == 'Cryoproof test') {
                    copy = `${height} ${event} <span class="snowflake">${SNOWFLAKE_EMOJI}</span>`;
                } else if (event == 'Tethered hop') {
                    copy += '&nbsp' + FLAME_EMOJI;
                }
                body = `<div class="single-line-item-event ${outcome_class} outcome cell-width">${copy}</div>`;
            }
        }

        return $(
            (willBoosterRowWrap ? '<br>' : '') +  // Wrap every n'th launch.
            `<div id="${launchId}" class="booster-launch-wrapper ${willBoosterRowWrap ? ' booster-row-wrap' : ''}" ${isNewBooster ? '' : ` style="${FADE_IN_START_STYLE}"`}>` +
                (isNewBooster ? '' : `<span class="launch-interim">${daysSinceLastLaunch}<br>&rarr;<br>${daysSinceLastLaunch == 1 ? 'day' : 'days'}</span>`) +
                `<div class="booster-launch td-cell cell-width">` +
                    `<div class="launch-date cell-width">${launch_datetime.substring(0, 10)}</div>` +
                    body +
                    // `<div class="landing outcome cell-width ${booster_landing_class}">${landing}</div>` +
                    // `<div class="badges cell-width"></div>` +
                `</div>` +
            `</div>`,
        );
    }
}
