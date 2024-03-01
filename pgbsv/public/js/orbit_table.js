
class OrbitTable {
    constructor(wrapperId, leftColor, rightColor) {
        this.wrapperId = wrapperId;
        this._wrapper = $(`#${this.wrapperId}`);
        this._leftColor = leftColor;
        this._rightColor = rightColor;

        // Make the storage for each orbit class.
        this._orbitClassTallies = _.object(_.map(ORBIT_CLASSES, (orbit) => {
            return [
                orbit,
                {
                    changedEver: false,
                    changedLeft: false,
                    changedRight: false,
                    // Launches and differentials.
                    numLeftLaunches: [0],
                    curNumLeftLaunches: 0,
                    numRightLaunches: [0],
                    curNumRightLaunches: 0,
                    // maxLaunchDifferential: [0,
                    // Payloads and differentials.
                    leftPayloadSum: [0],
                    curLeftPayloadSum: 0,
                    rightPayloadSum: [0],
                    curRightPayloadSum: 0,
                    // maxPayloadDifferential: 0,
                    // TODO: Calculate Bayesian estimate for classified masses? But doesn't work with singleton orbits. Oh well.
                    // Do this gold plating later, maybe.
                    // // Number of known payload masses.
                    // numPayloads: 0,
                    // // Sum of all known payload masses.
                    // payloadSum: 0,
                },
            ];
        }));
    }

    // // Gets the display class for an orbit string.
    // static getOrbitClass(orbitStr) {
    //     if (orbitStr == 'LEO' || orbitStr == 'ISS' || orbitStr == 'Sub-orbital') {
    //         return 'leo';
    //     } else if (orbitStr == 'SSO') {
    //         return 'sso';
    //     } else if (orbitStr == 'MEO' || orbitStr == 'HEO') {
    //         return 'heo';
    //     } else if (orbitStr == 'GEO' || orbitStr == 'GTO') {
    //         return 'geo';
    //     } else if (orbitStr == 'Lunar' || orbitStr == 'HTO' || orbitStr == 'L1' || orbitStr == 'Heliocentric' || orbitStr == 'L2') {
    //         return 'lunar';
    //     } else {
    //         throw `OrbitTable.getOrbitClass not implemented: ${orbitStr}`;
    //     }
    // }

    // Gets a payload mass using frequentist approximation.
    static getPayloadMass(rocket) {  // orbitStr, payloadMassKg) {
        // OrbitTable.getPayloadMass(rockets[0].orbit_str, rockets[0].payload_mass_kg),
        return rocket.payload_mass_kg || FREQUENTIST_PAYLOADS[rocket.orbit_str];
    }

    _getOrbitWrapperKey(orbitKey) {
        return `#${this.wrapperId} .dual-orbit-wrapper.${orbitKey} `;
    }

    _effectLinearGradient(selector, leftValue, rightValue, changedEver, progress) {
        if (leftValue + rightValue == 0) {
            return;
        }

        // var perc = 5 + 90 * leftValue / (leftValue + rightValue);
        var perc = 100.0 * leftValue / (leftValue + rightValue);
        if (!changedEver && (leftValue == 0 || rightValue == 0)) {
            // There will be no slide effect changing from one being zero, so mix in the progress as a prior to get the proper effect.
            perc = progress * perc + (1.0 - progress) * 50;
        }

        var leftColor = this._leftColor,
            rightColor = this._rightColor;
        // TODO: Doesn't work.
        // if (progress > 0 && progress < 1) {
        //     // Use more vivid colors.
        //     leftColor = 'rgb(180, 180, 228)';
        //     rightColor = 'rgb(228, 180, 180)';
        // }

        $(selector).css(
            'background-image',
            // `linear-gradient(to right, white 0%, ${this._leftColor} ${perc}%, ${this._rightColor} ${perc}%, white 100%)`,
            `linear-gradient(to right, rgba(0, 0, 0, 0) 0%, ${leftColor} ${perc}%, ${rightColor} ${perc}%, rgba(0, 0, 0, 0) 100%)`,
        );
    }

    _innerRender(progress) {
        // Render the counts!
        _.map(this._orbitClassTallies, (v, k) => {
            let keyPrefix = this._getOrbitWrapperKey(k);

            if (v.curNumLeftLaunches + v.curNumRightLaunches > 0) {
                // Always show 5% holdout on either side.
                this._effectLinearGradient(`${keyPrefix} .dual-launch-tally`, v.curNumLeftLaunches, v.curNumRightLaunches, v.changedEver, progress);
            }
            $(`${keyPrefix} .dual-launch-tally .left.count`).html(Math.ceil(v.curNumLeftLaunches));
            $(`${keyPrefix} .dual-launch-tally .right.count`).html(Math.ceil(v.curNumRightLaunches));

            if (v.curLeftPayloadSum + v.curRightPayloadSum > 0) {
                this._effectLinearGradient(`${keyPrefix} .dual-payload-sum`, v.curLeftPayloadSum, v.curRightPayloadSum, v.changedEver, progress);
            }
            $(`${keyPrefix} .dual-payload-sum .left.count`).html(`${numberWithCommas(Math.round(v.curLeftPayloadSum))} kg`);
            $(`${keyPrefix} .dual-payload-sum .right.count`).html(`${numberWithCommas(Math.round(v.curRightPayloadSum))} kg`);
            // TODO: Color based on the balance of power using a linear gradient, yeah.
        });
    }

    // Gets a mixed value from a cumulative array based on a [0, 1.0] animation progress.
    _cumArrayMixedValue(arr, progress) {
        if (arr.length == 1) {
            return arr[0];
        }

        let prev = arr[arr.length - 2],
            next = arr[arr.length - 1],
            value = prev + progress * (next - prev);
        // Only round for the first or last values.
        return progress == Math.round(progress) ? Math.round(value) : value;
    }

    _updateCurrentTallies(progress) {
        _.each(this._orbitClassTallies, (v, k) => {
            if (v.changedLeft) {
                v.curNumLeftLaunches = this._cumArrayMixedValue(v.numLeftLaunches, progress);
                v.curLeftPayloadSum = this._cumArrayMixedValue(v.leftPayloadSum, progress);
            } else {
                v.curNumLeftLaunches = v.numLeftLaunches[v.numLeftLaunches.length - 1];
                v.curLeftPayloadSum = v.leftPayloadSum[v.leftPayloadSum.length - 1];

            }

            if (v.changedRight) {
                v.curNumRightLaunches = this._cumArrayMixedValue(v.numRightLaunches, progress);
                v.curRightPayloadSum = this._cumArrayMixedValue(v.rightPayloadSum, progress);
            } else {
                v.curNumRightLaunches = v.numRightLaunches[v.numRightLaunches.length - 1];
                v.curRightPayloadSum = v.rightPayloadSum[v.rightPayloadSum.length - 1];
            }
        });
    }

    render(closure) {
        if (!_.some(this._orbitClassTallies, (t) => t.changedLeft || t.changedRight)) {
            // Nothing is changed, so just render as-is once.
            this._updateCurrentTallies(1.0);
            this._innerRender(1.0);
            return;
        }

        // Step-wise animate the changed ones up.
        let animationFrames = 24;
        var animationIx = 0;

        // Mark all animating things with CSS class.
        _.each(this._orbitClassTallies, (t, k) => {
            if (t.changedLeft || t.changedRight) {
                $(this._getOrbitWrapperKey(k)).addClass(t.changedLeft ? 'changing-left' : 'changing-right');
            }
        });

        var animationClosure = () => {
            if (animationIx > animationFrames) {
                // Mark all as un-changed.
                _.each(this._orbitClassTallies, (t, k) => {
                    // setTimeout(() => $(this._getOrbitWrapperKey(k)).removeClass('changing-left changing-right'), 400);
                    $(this._getOrbitWrapperKey(k)).removeClass('changing-left changing-right');
                    t.changedEver = t.changedEver || t.changedLeft || t.changedRight;
                    t.changedLeft = false;
                    t.changedRight = false;
                });
                return;
            }

            let progress = 1.0 * animationIx / animationFrames;
            this._updateCurrentTallies(progress);
            this._innerRender(progress);
            ++animationIx;
            setTimeout(animationClosure, 30);
        };
        animationClosure();
    }

    _cumArrayPush(arr, value) {
        arr.push(arr[arr.length - 1] + value);
    }

    // Adds a rocket launch for the left or right side for the given orbit string and payload mass.
    addRocketLaunch(isRight, orbitClass, payloadKg) {
        // let orbitClass = OrbitTable.getOrbitClass(orbitStr),
        const tallies = this._orbitClassTallies[orbitClass];
        if (isRight) {
            tallies.changedRight = true;
            this._cumArrayPush(tallies.numRightLaunches, 1);
            if (payloadKg != null) {
                this._cumArrayPush(tallies.rightPayloadSum, payloadKg);
            }
        } else {
            tallies.changedLeft = true;
            this._cumArrayPush(tallies.numLeftLaunches, 1);
            if (payloadKg != null) {
                this._cumArrayPush(tallies.leftPayloadSum, payloadKg);
            }
        }

        // tallies.maxLaunchDifferential = Math.max(
        //     tallies.maxLaunchDifferential,
        //     Math.abs(tallies.numRightLaunches - tallies.numLeftLaunches),
        // );
        // tallies.maxPayloadDifferential = Math.max(
        //     tallies.maxPayloadDifferential,
        //     Math.abs(tallies.rightPayloadSum - tallies.leftPayloadSum),
        // );
    }
}
