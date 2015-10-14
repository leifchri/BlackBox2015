/*
Bugs: Nstep entry box doesn't work on Firefox, currentStep only updates for step()
*/

var gl;
var vPosition;
var uColor;

var grid = [];
var prevGrid = [];
var gridXY = [];

var chars = [];
var n = 1;
var currentStep = 0;
var currentLabel;

var label;

window.onload = function init() {
    label = document.getElementById("debug-label");
    label.innerHTML = "n = " + n.toString();

    for (y = 0.855; y > -.9; y = y - 0.09) {
        for (x = -0.855; x < 0.9; x = x + 0.09) {
            gridXY.push(vec2(x, y));
        }
    }

	currentLabel = document.getElementById("current-step");
    var nButton = document.getElementById("nStep");

    nButton.addEventListener("keypress", function(ev) {
        if (ev.keyCode != 13) {
            chars.push(String.fromCharCode(ev.keyCode));
        }
    });
    nButton.addEventListener("keyup", function(ev) {
        if (ev.keyCode == 13) {
            nButton.value = chars.join('');
            n = parseInt(nButton.value);
            chars = [];
            label.innerHTML = "n = " + n.toString();
        }
    });

    var canvas = document.getElementById("gl-canvas");

    gl = WebGLUtils.setupWebGL(canvas);
    if (!gl) { alert("WebGL isn't available"); }

    //
    //  Configure WebGL
    //
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    //  Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Load the data into the GPU
    var bufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufferId);

    // Associate our shader variables with our data buffer
    vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    // Get pointers to the color variables
    uColor = gl.getUniformLocation(program, "uColor");

    reset();
}

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT);

    var p = 0;
    gl.bufferData(gl.ARRAY_BUFFER, flatten(gridXY), gl.STATIC_DRAW);
    try {
        for (i = 0; i < 20; i++) {
            for (j = 0; j < 20; j++) {
                var color = getColor(grid[i][j]);
                //gl.uniform4f(uColor, color.r, color.g, color.b, 1.0);
                gl.uniform4f(uColor, color[0], color[1], color[2], 1.0);
                gl.drawArrays(gl.POINTS, p, 1);
                p++;
            }
        }
    }
    catch (TypeError) {
        for (i = 0; i < 20; i++) {
            for (j = 0; j < 20; j++) {
                gl.uniform4f(uColor, 0, 1, 1, 1.0);
                gl.drawArrays(gl.POINTS, p, 1);
                p++;
            }
        }
    }
}

function reset() {
    prevGrid = jQuery.extend(true, [], grid);
    grid = [];
    for (i = 0; i < 20; i++) {
        var row = [];
        for (j = 0; j < 20; j++) {
            row.push(Math.floor(Math.random() * 10));
        }
        grid.push(row);
    }
    currentStep = 0;
    render();
}

function revert() {
    var temp = jQuery.extend(true, [], grid);
    grid = prevGrid = jQuery.extend(true, [], prevGrid);
    prevGrid = jQuery.extend(true, [], temp);
    render();
}

function step_it() {
	currentStep = currentStep + n;
    currentLabel.innerHTML = "Current step: " + currentStep.toString();
    prevGrid = [];
    prevGrid = jQuery.extend(true, [], grid);
    for (i = 0; i < n; i++) {
        step1();
    }
    render();
}

function step1() {
    var x, y;
    //var l, r, u, d;
    //Q1
    /*for (i = 0; i < 10; i++) {
        for (j = 0; j < 10; j++) {
            grid[i][j] = 0;
        }
    }*/
    //Q2
    x = Math.floor(Math.random() * 10);
    y = Math.floor(Math.random() * 10 + 10);
    rand = Math.floor(Math.random() * 100)
    if (grid[x][y] == 0) {
    } else if ( (grid[x][y] == 5) || (rand < 30) ) {
        grid[x][y] = 0;
    } else if ((grid[x][y]%2) == 0) {
        grid[x][y] = (grid[x][y] + 2*rand)%10;
    } else {
        grid[x][y] = (grid[x][y] + rand)%10;
    }
    /*for (i = 0; i < 10; i++) {
        for (j = 10; j < 20; j++) {
            grid[i][j] = 0;
        }
    }*/
    //Q3
    /*for (i = 10; i < 20; i++) {
        for (j = 0; j < 10; j++) {
            grid[i][j] = 0;
        }
    }*/
    //Q4
    //Not that in this case x refers to row and y to column
    x = Math.floor(Math.random() * 10 + 10);
    y = Math.floor(Math.random() * 10 + 10);
    if (grid[x][y] == 0) {
        try {
            var p1 = grid[x - 1][y];
        } catch (typeError) {}
        //catch (TypeError) {
       //}
        try {
            var p2 = grid[x][y - 1];
        } catch (typeError) {}
        try {
            var p3 = grid[x + 1][y];
        } catch (typeError) {}
        try {
            var p4 = grid[x][y + 1];
        } catch (typeError) { }
        // Need to make sure this is instide of right quadrant
        //if there is an adjacent pixel that is not orange or black
        if (x == 10) {
            if (y == 10) {
                if (((p3 % 7) != 0) || ((p4 % 7) != 0)) {
                    grid[x][y] = 6;
                }
            } else if (y == 20) {
                if (((p2 % 7) != 0) || ((p3 % 7) != 0)) {
                    grid[x][y] = 6;
                }
            } else {
                if (((p2 % 7) != 0) || ((p3 % 7) != 0) || ((p4 % 7) != 0)) {
                    grid[x][y] = 6;
                }
            }
        } else if (x == 20) {
            if (y == 10) {
                if (((p1 % 7) != 0) || ((p4 % 7) != 0)) {
                    grid[x][y] = 6;
                }
            } else if (y == 20) {
                if (((p1 % 7) != 0) || ((p2 % 7) != 0)) {
                    grid[x][y] = 6;
                }
            } else {
                if (((p1 % 7) != 0) || ((p2 % 7) != 0) || ((p4 % 7) != 0)) {
                    grid[x][y] = 6;
                }
            }
        } else {
            if (((p1 % 7) != 0) || ((p2 % 7) != 0) || ((p3 % 7) != 0) || ((p4 % 7) != 0)) {    
                grid[x][y] = 6;
            }
        }
        
        //grid[x][y] = 6;
        
    } else if (grid[x][y] == 6) {
        grid[x][y] = 7;
    } else if (grid[x][y] == 7) {
        grid[x][y] = 0;   
    } else if ((grid[x][y] % 2) == 1) {
        grid[x][y] = 7;
    } else {
        grid[x][y] = 0;
    }
    //if (grid[x][y]%
    /*for (i = 10; i < 20; i++) {
        for (j = 10; j < 20; j++) {
            if (grid[x][y] == 0) {
                grid[x][y] = 9;
            }
        }
    }*/
}

function getColor(num) {
    if (num == 0) {
        r = 0; g = 0; b = 0;
    } else if (num == 1) {
        r = 0.5; g = 0.5; b = 0.5;
    } else if (num == 2) {
        r = 0; g = 0; b = 1;
    } else if (num == 3) {
        r = 1; g = 0; b = 1;
    } else if (num == 4) {
        r = 0; g = 1; b = 1;
    } else if (num == 5) {
        r = 0; g = 0.5; b = 0;
    } else if (num == 6) {
        r = 1; g = 0; b = 0;
    } else if (num == 7) {
        r = 1; g = 0.65; b = 00;
    } else if (num == 8) {
        r = 1; g = 0.75; b = 0.8;
    } else if (num == 9) {
        r = 1; g = 1; b = 1;
    } else if (num == 10) {
       r = 1; g = 1; b = 0;
    }
    return [r, g, b];
}