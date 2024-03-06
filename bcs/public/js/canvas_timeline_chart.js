
class CanvasTimelineChart {
    static canvasLeftAxisMargin = 40;

    static yBoundsDefault = {
        yMin: -5,
        yMax: 5,
        yStep: 5,
    };
    static colorsDefault = {
        positiveRgb: '128, 128, 255',
        positiveLineRgb: '0, 0, 255',
        negativeRgb: '255, 128, 128',
        negativeLineRgb: '255, 0, 0',
    };

    constructor(timelineId, minDatetime, maxDatetime, opt_options) {
        // Div ID to display the timeline in.
        this.timelineId = timelineId;
        this.minDatetime = minDatetime;
        this.maxDatetime = maxDatetime;

        let options = opt_options || {};

        this.colors = options.colors || CanvasTimelineChart.colorsDefault;
        // TODO: Not implemented.

        let yBounds = options.yBounds || {};
        this.yMin = yBounds.yMin !== undefined ? yBounds.yMin : CanvasTimelineChart.yBoundsDefault.yMin;
        this.yMax = yBounds.yMax !== undefined ? yBounds.yMax : CanvasTimelineChart.yBoundsDefault.yMax;
        this.yStep = yBounds.yStep !== undefined ? yBounds.yStep : CanvasTimelineChart.yBoundsDefault.yStep;
        // If we need to draw new y bounds, we cache them here.
        this._newYBounds = null;
        this._newMaxDatetime = null;

        this._drawInverted = options.drawInverted !== undefined ? options.drawInverted : false;
        this._drawXTicks = options.drawXTicks !== undefined ? options.drawXTicks : true;
        this._drawXMonthlyBars = options.drawXMonthlyBars !== undefined ? options.drawXMonthlyBars : false;
        this._drawYTicks = options.drawYTicks !== undefined ? options.drawYTicks : true;
        this._xTicksBelow = options.xTicksBelow !== undefined ? options.xTicksBelow : false;
        this._gridColor = 'gray';
        this._useGradient = options.useGradient !== undefined ? options.useGradient : true;

        // this._shadeMonthly = options.shadeMonthly || false;
        // this._shadeMonthly = options.shadeMonthly || false;

        this._canvasTopMargin = options.canvasTopMargin !== undefined ? options.canvasTopMargin : 16;

        this.height = options.height || $(`#${this.timelineId}`).height();
        this.width = options.width || $(`#${this.timelineId}`).width();

        console.log(`Timeline chart dims: ${this.width} x ${this.height}`);

        // this._namedSeriesBarWidth = options.namedSeriesBarWidth !== undefined ? options.namedSeriesBarWidth : 14;
        // this._namedSeriesBarPadding = options.namedSeriesBarPadding !== undefined ? options.namedSeriesBarPadding : 14;
        // // List of named series with metadata:
        // // * name: String
        // // * events: Array[ ... things? ]
        // this._namedSeries = [];
        // this._namedSeriesMap = {};
        // this._namedSeriesPreviousMaxDatetime = this.minDatetime;
        // this._namedSeriesMaxDatetime = this.minDatetime;

        this._canvas = document.getElementById(this.timelineId);
        const scale = window.devicePixelRatio; // Change to 1 on retina screens to see blurry canvas.
        this._canvas.width = Math.floor(this.width * scale);
        this._canvas.height = Math.floor(this.height * scale);
        // console.log(`Actual canvas dims: ${this._canvas.width} x ${this._canvas.height}`);
        this._canvas.getContext('2d').scale(scale, scale);
    }

    _clearCanvas() {
        var ctx = this._canvas.getContext('2d');
        ctx.clearRect(0, 0, this.width, this.height);
    }

    _convertDatetimeToX(datetime) {
        return Math.round(
            CanvasTimelineChart.canvasLeftAxisMargin +
            (this.width - CanvasTimelineChart.canvasLeftAxisMargin) * (+datetime - +this.minDatetime) / (+this.maxDatetime - +this.minDatetime)
        );
    }

    _convertPointValueToY(pointValue) {
        if (this._drawInverted) {
            // y=0 at the top and going down.
            return Math.round(
                this._canvasTopMargin +
                (this.height - 2 * this._canvasTopMargin) * (pointValue - this.yMin) / (this.yMax - this.yMin)
            );
        } else {
            // y=0 at the bottom and going up.
            return Math.round(
                this._canvasTopMargin +
                (this.height - 2 * this._canvasTopMargin) -
                (this.height - 2 * this._canvasTopMargin) * (pointValue - this.yMin) / (this.yMax - this.yMin)
            );
        }
    }

    // Draw date ticks along x axis.
    _doDrawXTicks(ctx, yOrigin, maxYValue) {
        ctx.textAlign = 'left';
        ctx.fillStyle = this._gridColor;
        ctx.font = '12px Arial';
        let cursorTextXOffset = this._xTicksBelow ? 0 : 0,
            cursorTextY = this._convertPointValueToY(0) + (this._xTicksBelow ? 12 : -4);
        if (this.minDatetime.getMonth() == 0) {
            // Draw this.
            ctx.fillText(this.minDatetime.getFullYear(), cursorTextXOffset + CanvasTimelineChart.canvasLeftAxisMargin + 3, cursorTextY);
        }
        var cursorYear = this.minDatetime.getFullYear() + 1,
            cursorDate = new Date(cursorYear, 0, 1, 0, 0, 0);
        while (+cursorDate <= +this.maxDatetime) {
            let cursorX = cursorTextXOffset + this._convertDatetimeToX(cursorDate) + 3;
            ctx.fillText(cursorDate.getFullYear(), cursorX, cursorTextY);
            // Draw tick.
            ctx.beginPath();
            ctx.moveTo(cursorX - 3, yOrigin);
            ctx.lineTo(cursorX - 3, yOrigin + 5);
            ctx.stroke();

            cursorYear += 1;
            cursorDate = new Date(cursorYear, 0, 1, 0, 0, 0);
        }

        // Also draw months and quarters as needed?
        if (this._drawXMonthlyBars) {
            var year = this.minDatetime.getFullYear(),
                month = this.minDatetime.getMonth();
            ctx.strokeStyle = 'lightgray';
            while (year < this.maxDatetime.getFullYear() ||
                    year == this.maxDatetime.getFullYear() && month < this.maxDatetime.getMonth()) {
                let newX = this._convertDatetimeToX(new Date(year, month, 1, 0, 0, 0));
                ctx.beginPath();
                ctx.moveTo(newX, this._canvasTopMargin);
                ctx.lineTo(newX, maxYValue);
                ctx.stroke();

                if (month == 11) {
                    year += 1;
                    month = 0;
                } else {
                    month += 1;
                }
            }
        }
    }

    _drawAxes() {
        var ctx = this._canvas.getContext('2d');
        ctx.strokeStyle = ctx.fillStyle = this._gridColor;

        // y axis.
        let maxYValue = this.height - this._canvasTopMargin;
        ctx.beginPath();
        ctx.moveTo(CanvasTimelineChart.canvasLeftAxisMargin, this._canvasTopMargin);
        ctx.lineTo(CanvasTimelineChart.canvasLeftAxisMargin, maxYValue);
        ctx.stroke();

        // x axis.
        let yOrigin = this._convertPointValueToY(0);
        ctx.beginPath();
        ctx.moveTo(CanvasTimelineChart.canvasLeftAxisMargin, yOrigin);
        ctx.lineTo(this.width, yOrigin);
        ctx.stroke();

        if (this._drawXTicks) {
            this._doDrawXTicks(ctx, yOrigin, maxYValue);
        }

        if (this._drawYTicks) {
            // Draw value ticks along y axis.
            // let yTickSpacing = Math.max(5, 5 * Math.round(Math.round((this.yMax - this.yMin) / 5) / 5));
            let yTickSpacing = Math.max(1, 5 * Math.round(Math.round((this.yMax - this.yMin) / 8) / 5));
            let yTickX = CanvasTimelineChart.canvasLeftAxisMargin;
            ctx.fillStyle = this._gridColor;
            ctx.font = '12px Arial';
            ctx.textAlign = 'right';
            for (
                var yTick = Math.floor(this.yMin / yTickSpacing) * yTickSpacing;
                yTick <= Math.floor(this.yMax / yTickSpacing) * yTickSpacing;
                yTick += yTickSpacing
            ) {
                let yValue = this._convertPointValueToY(yTick);
                if (yValue > maxYValue) {
                    continue;
                }

                ctx.fillText(Math.abs(yTick), CanvasTimelineChart.canvasLeftAxisMargin - 8, yValue + 3);
                // Draw tick.
                ctx.beginPath();
                ctx.moveTo(CanvasTimelineChart.canvasLeftAxisMargin - 5, yValue);
                ctx.lineTo(CanvasTimelineChart.canvasLeftAxisMargin, yValue);
                ctx.stroke();
            }
        }
    }

    _subRender(isTerminalRender) {
        // Do nothing.
    }

    // _innerRender(hideLastPoint, closure) {
    // `isTerminalRender`: Whether the chart will be fixed after rendering of this is transitional.
    _innerRender(isTerminalRender, closure) {
        this._clearCanvas();
        this._drawAxes();
        this._subRender(isTerminalRender);
        closure();
    }

    _getPreRenderBlob() {
        return {
            'CanvasTimelineChart': {
                curYMin: this.yMin,
                curYMax: this.yMax,
                newYMin: this._newYBounds ? this._newYBounds[0] : this.yMin,
                newYMax: this._newYBounds ? this._newYBounds[1] : this.yMax,
                oldMaxDatetime: this.maxDatetime,
                newMaxDatetime: this._newMaxDatetime != null ? this._newMaxDatetime : this.maxDatetime,
            },
        };
    }

    _midRender(preRenderBlob, animationProgress) {
        let {
            curYMin,
            curYMax,
            newYMin,
            newYMax,
            oldMaxDatetime,
            newMaxDatetime,
        } = preRenderBlob['CanvasTimelineChart'];
        this.yMin = curYMin + animationProgress * (newYMin - curYMin);
        this.yMax = curYMax + animationProgress * (newYMax - curYMax);
        this.maxDatetime = new Date(
            Math.max(
                +this.maxDatetime,
                // +this._namedSeriesMaxDatetime + 86400000 * 30,
                +(new Date(+oldMaxDatetime + animationProgress * (+newMaxDatetime - +oldMaxDatetime))),
            ),
        );
    }

    _postRender(preRenderBlob) {
        let { newYMin, newYMax, newMaxDatetime } = preRenderBlob['CanvasTimelineChart'];
        this.yMin = newYMin;
        this.yMax = newYMax;
        this._newYBounds = null;
        this._newMaxDatetime = null;
        this.maxDatetime = newMaxDatetime;
    }

    render(closure) {
        let numAnimationSteps = FAST_MODE ? 0 : 20,
            animationDelay = 8;
        // if (this._newYBounds == null) {
        // } else {
        // Progressively update the y bounds first, then draw the new point.
        let
            // curYMin = this.yMin,
            // curYMax = this.yMax,
            // newYMin = this._newYBounds ? this._newYBounds[0] : this.yMin,
            // newYMax = this._newYBounds ? this._newYBounds[1] : this.yMax,
            // Don't render the new point until we're at the end of the animation.
            // top = this.series.pop(),
            // lastSeriesPoint = this.series.length ? this.series[this.series.length - 1] : [top[0], top[1]],
            preRenderBlob = this._getPreRenderBlob();

            // Don't fully update the datetime scaling till the end, either.
            // oldMaxDatetime = this.maxDatetime,
            // newMaxDatetime = this._newMaxDatetime != null ? this._newMaxDatetime : this.maxDatetime;
            // newNamedSeriesMaxDatetime = this._namedSeriesMaxDatetime;
        // Clear the new y bounds so we don't infinite-loop.

        var animationClosure = (() => {
            var animationIx = 0;
            return () => {
                if (animationIx == numAnimationSteps) {
                    // Restore the state of the chart and render with the original closure.
                    // this.yMin = newYMin;
                    // this.yMax = newYMax;
                    // // this.series.push(top);
                    this._postRender(preRenderBlob);
                    // this._newMaxDatetime = null;
                    // this.maxDatetime = newMaxDatetime;
                    this._innerRender(true, closure);
                } else {
                    // Update the y bounds progressively and add an interpolated point.
                    animationIx += 1;
                    let animationProgress = animationIx / numAnimationSteps;
                    // this.yMin = curYMin + animationProgress * (newYMin - curYMin);
                    // this.yMax = curYMax + animationProgress * (newYMax - curYMax);
                    // // this._namedSeriesMaxDatetime = new Date(
                    // //     +this._namedSeriesPreviousMaxDatetime +
                    // //     animationProgress * (+newNamedSeriesMaxDatetime - +this._namedSeriesPreviousMaxDatetime)
                    // // );
                    // this.maxDatetime = new Date(
                    //     Math.max(
                    //         +this.maxDatetime,
                    //         // +this._namedSeriesMaxDatetime + 86400000 * 30,
                    //         +(new Date(+newMaxDatetime + animationProgress * (+newMaxDatetime - +newMaxDatetime))),
                    //     ),
                    // );

                    // this.series.push([
                    //     lastSeriesPoint[0] + animationProgress * (top[0] - lastSeriesPoint[0]),
                    //     new Date(
                    //         +lastSeriesPoint[1] + animationProgress * (+top[1] - +lastSeriesPoint[1]),
                    //     ),
                    // ]);
                    this._midRender(preRenderBlob, animationProgress);

                    // Render with the same continuation after a delay.
                    setTimeout(() => {
                        this._innerRender(false, () => {
                            // Clear the synthetic point before the next loop.
                            // this.series.pop();
                            animationClosure();
                        });
                    }, animationDelay);
                }
            };
        })();
        animationClosure();
    }

    setNewYBounds(newYMin, newYMax) {
        this._newYBounds = [newYMin, newYMax];
    }
}

class AreaTimelineChart extends CanvasTimelineChart {
    constructor(timelineId, minDatetime, maxDatetime, opt_options) {
        super(timelineId, minDatetime, maxDatetime, opt_options);

        this.seriesPointValueMin = 0;
        this.seriesPointValueMax = 0;
        // List of series points, which are tuples of values and datetimes.
        this.series = [[0, this.minDatetime]];
    }

    _getPreRenderBlob() {
        var preRenderBlob = super._getPreRenderBlob();

        // let top = this.series.pop();
        let top = this.series[this.series.length - 1];
        preRenderBlob['AreaTimelineChart'] = {
            top,
            lastSeriesPoint: this.series.length >= 2 ? this.series[this.series.length - 2] : top.slice(0),  // [top[0], top[1]],
        };
        return preRenderBlob;
    }

    _midRender(preRenderBlob, animationProgress) {
        super._midRender(preRenderBlob, animationProgress);

        let { top, lastSeriesPoint } = preRenderBlob['AreaTimelineChart'];
        // Create an intermediate point.
        this.series.pop();
        this.series.push([
            lastSeriesPoint[0] + animationProgress * (top[0] - lastSeriesPoint[0]),
            new Date(+lastSeriesPoint[1] + animationProgress * (+top[1] - +lastSeriesPoint[1])),
            top[2],
        ]);
    }

    _postRender(preRenderBlob) {
        super._postRender(preRenderBlob);

        let { top } = preRenderBlob['AreaTimelineChart'];
        // Restore the right point.
        this.series.pop();
        this.series.push(top);
    }

    recordRelativeMove(relative, datetime, opt_options) {
        this.series.push([this.series[this.series.length - 1][0] + relative, datetime, opt_options || {}]);
        let pointValue = this.series[this.series.length - 1][0];

        var newYMin = this.yMin,
            newYMax = this.yMax;
        while (pointValue < newYMin) {
            newYMin -= this.yStep;
        }

        while (pointValue > newYMax) {
            newYMax += this.yStep;
        }

        this.seriesPointValueMin = Math.min(this.seriesPointValueMin, pointValue);
        this.seriesPointValueMax = Math.max(this.seriesPointValueMax, pointValue);
        this.setNewYBounds(newYMin, newYMax);
        return pointValue;
    }

    // Draws all `_series` points.
    // :param hideLastPoint: Whether to not render the last point yet (but do render its area).
    _drawPoints(hideLastPoint) {
        if (this.series.length == 1) {
            return;
        }

        const ctx = this._canvas.getContext('2d'),
            xys = [];
        ctx.strokeStyle = ctx.fillStyle = this._gridColor;
        // Draw area chart under the curve.
        for (let i = 0; i < this.series.length; ++i) {
            const pointValue = this.series[i][0],
                datetime = this.series[i][1],
                optionsI = this.series[i][2],
                x = this._convertDatetimeToX(datetime),
                y = this._convertPointValueToY(pointValue),
                point0y = this._convertPointValueToY(0);
            xys.push([x, y, pointValue]);
            // console.log(`${pointValue} ${datetime} XY ${x},${y}`);

            if (xys.length >= 2) {
                const l = xys.length,
                    x1 = xys[l - 2][0],
                    y1 = xys[l - 2][1],
                    x2 = xys[l - 1][0],
                    y2 = xys[l - 1][1],
                    maxOpacity = 45,
                    pointMagnitude = Math.max(Math.abs(this.seriesPointValueMin), Math.abs(this.seriesPointValueMax)),
                    biPoint = pointValue || xys[l - 2][2];
                const gradient = ctx.createLinearGradient(
                    x2,
                    point0y,
                    x2,
                    this._convertPointValueToY((Math.sign(pointValue) || Math.sign(xys[l - 2][2])) * pointMagnitude),
                );

                let rgb = null;
                if (optionsI != null && optionsI.rgb) {
                    rgb = optionsI.rgb;
                } else if (i > 0 && this.series[i][0] < this.series[i - 1][0]) {
                    // gradient = ctx.createLinearGradient(x2, point0y, x2, this._convertPointValueToY(this.seriesPointValueMin));
                    // let biPoint = pointValue || xys[l - 2][2];
                    // gradient.addColorStop(0, `rgba(${this.colors.negativeRgb}, 0)`);
                    // gradient.addColorStop(1, `rgba(${this.colors.negativeRgb}, ${(maxOpacity * Math.abs(biPoint) / pointMagnitude) || 0})`);
                    rgb = this.colors.negativeRgb;
                } else {
                    // gradient.addColorStop(0, `rgba(${this.colors.positiveRgb}, 0)`);
                    // gradient.addColorStop(1, `rgba(${this.colors.positiveRgb}, ${(maxOpacity * Math.abs(pointValue) / pointMagnitude) || 0})`);
                    rgb = this.colors.positiveRgb;
                }
                if (!this._useGradient || optionsI != null && optionsI.useGradient === false) {
                    gradient.addColorStop(0, `rgba(${rgb}, ${maxOpacity / 100.0})`);
                    gradient.addColorStop(1, `rgba(${rgb}, ${maxOpacity / 100.0})`);
                } else {
                    gradient.addColorStop(0, `rgba(${rgb}, 0)`);
                    gradient.addColorStop(1, `rgba(${rgb}, ${(maxOpacity * Math.abs(biPoint) / pointMagnitude) || 0})`);
                }
                ctx.fillStyle = gradient;

                ctx.beginPath();
                ctx.moveTo(x1, point0y);
                ctx.lineTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.lineTo(x2, point0y);
                ctx.closePath();
                ctx.fill();
            }
        }

        // Draw lines connecting points.
        for (var i = 1; i < this.series.length; ++i) {
            const pointValue = this.series[i][0],
                datetime = this.series[i][1],
                optionsI = this.series[i][2],
                x = this._convertDatetimeToX(datetime),
                y = this._convertPointValueToY(pointValue),
                point0y = this._convertPointValueToY(0);

            if (optionsI != null && optionsI.lineRgb) {
                ctx.strokeStyle = ctx.fillStyle = `rgb(${optionsI.lineRgb})`;
            } else if (this.series[i][0] >= this.series[i - 1][0]) {
                ctx.strokeStyle = ctx.fillStyle = `rgb(${this.colors.positiveLineRgb})`;
            } else {
                ctx.strokeStyle = ctx.fillStyle = `rgb(${this.colors.negativeLineRgb})`;
            }

            const x1 = xys[i - 1][0],
                y1 = xys[i - 1][1],
                x2 = xys[i][0],
                y2 = xys[i][1];
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }

        // Draw points on top.
        for (var i = 0; i < this.series.length; ++i) {
            const pointValue = this.series[i][0],
                datetime = this.series[i][1],
                optionsI = this.series[i][2],
                x = this._convertDatetimeToX(datetime),
                y = this._convertPointValueToY(pointValue),
                point0y = this._convertPointValueToY(0);

            // Draw the points themselves connected by lines.
            if (!hideLastPoint || i < this.series.length - 1) {
                let rgb = null;
                if (i == 0) {
                    // rgb = this._gridColor;
                    rgb = '128, 128, 128';
                } else if (optionsI != null && optionsI.lineRgb) {
                    rgb = optionsI.lineRgb;
                } else if (i >= 1 && this.series[i][0] >= this.series[i - 1][0]) {
                    rgb = this.colors.positiveLineRgb;
                } else {
                    rgb = this.colors.negativeLineRgb;
                }

                ctx.strokeStyle = ctx.fillStyle = `rgb(${rgb})`;
                ctx.fillRect(x - 2, y - 2, 5, 5);
            }
        }
    }

    _subRender(isTerminalRender) {
        this._drawPoints(/*hideLastPoint=*/ !isTerminalRender);
    }
}
