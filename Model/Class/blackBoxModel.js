/*********************************************************************
Javascript for a webpage that implements our proposed model for the functioning of the 
BlackBox (http://www.informatics.indiana.edu/rocha/blackbox/BlackBox_N.php).

Q1, Q2, and Q4 are functional. Q1 and Q2 implement statistical models and Q4 implements
a rule based model.

The user can input a trial run (trial runs can be found here https://github.com/leifchri/BlackBox2015/tree/master/Scripts/TestFiles)
and the BlackBox will run, notifying the user of any disagreements between the model's state 
and the recorded state in the trial

Bugs: Nstep entry box doesn't work on Firefox
**********************************************************************/

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
var allText;
var seedFlag = 0;
var textLoc = 0;
var errors = 0;

var label;

window.onload = function init() {
    label = document.getElementById("debug-label");
    label.innerHTML = "n = " + n.toString();

    initGrid();

    initButtons();	

    //initFileInput();

    // Find WebGL context
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
        for (var i = 0; i < 20; i++) {
            for (var j = 0; j < 20; j++) {
                var color = getColor(grid[i][j]);
                //gl.uniform4f(uColor, color.r, color.g, color.b, 1.0);
                gl.uniform4f(uColor, color[0], color[1], color[2], 1.0);
                gl.drawArrays(gl.POINTS, p, 1);
                p++;
            }
        }
    }
    catch (TypeError) {
        for (var i = 0; i < 20; i++) {
            for (var j = 0; j < 20; j++) {
                gl.uniform4f(uColor, 0, 1, 1, 1.0);
                gl.drawArrays(gl.POINTS, p, 1);
                p++;
            }
        }
        label.innerHTML = "Caught it"
    }
    gl.uniform4f(uColor, 1, 1, 1, 1.0);
    gl.drawArrays(gl.LINES, p, 4);
}

function step_it() {
    currentStep = currentStep + n;
    currentLabel.innerHTML = "Current step: " + currentStep.toString();
    prevGrid = [];
    prevGrid = jQuery.extend(true, [], grid);
    for (var i = 0; i < n; i++) {
        step1();
    }
    if(seedFlag == 0) {
        render();
    }
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
    x = Math.floor(Math.random() * 10);
    y = Math.floor(Math.random() * 10);
    rand = Math.random();
	if (rand < .45) {
		grid[x][y] = 0;
	} else if (rand < .67) {
		grid[x][y] = 1;
	} else if (rand < .80) {
		grid[x][y] = 2;
	} else if (rand < .85) {
		grid[x][y] = 3;
	} else if (rand < .88) {
		grid[x][y] = 4;
	} else if (rand < .91) {
		grid[x][y] = 5;
	} else if (rand < .94) {
		grid[x][y] = 6;
	} else if (rand < .95) {
		grid[x][y] = 7;
	} else if (rand < .96) {
		grid[x][y] = 8;
	} else {
		grid[x][y] = 9;
	}
    //Q2
    x = Math.floor(Math.random() * 10);
    y = Math.floor(Math.random() * 10 + 10);
    rand = Math.floor(Math.random() * 10)
    if (grid[x][y] == 0) {
    } else if (grid[x][y] == 5) {
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
    if (seedFlag == 1) {
        textLoc1 = textLoc;
        var flagFound = 0;
        for (var i = 0; i < 100; i++) {
            if ( allText[textLoc1+i] != allText[textLoc1+100+i] ) {
                y = i % 10 + 10;
                x = (i - (y - 10))*1.0/10 + 10;
                flagFound = 1;
                console.log("step: " + currentStep)
                //console.log(allText[textLoc1+i] + " changed to " + allText[textLoc1+100+i] )
            }
        }
        if (flagFound == 0) {
            return;
        }
        textLoc+=100;
        //r = confirm("Continue?")
        console.log(x + " " + y)
    } else {
        x = Math.floor(Math.random() * 10 + 10);
        y = Math.floor(Math.random() * 10 + 10);
    }
    //console.log("x: " + x + " y: " + y)
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
        grid[x][y] = 0;
    } else {
        grid[x][y] = 7;
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

function revert() {
    var temp = jQuery.extend(true, [], grid);
    grid = prevGrid = jQuery.extend(true, [], prevGrid);
    prevGrid = jQuery.extend(true, [], temp);
    render();
}

function reset() {
    prevGrid = jQuery.extend(true, [], grid);
    grid = [];
    for (var i = 0; i < 20; i++) {
        var row = [];
        for (var j = 0; j < 20; j++) {
            row.push(Math.floor(Math.random() * 10));
        }
        grid.push(row);
    }

    render();
}

function initGrid() {
    for (var y = 0.855; y > -.9; y = y - 0.09) {
        for (var x = -0.855; x < 0.9; x = x + 0.09) {
            gridXY.push(vec2(x, y));
        }
    }
    var lines = [
        vec2(0,1),
        vec2(0,-1),
        vec2(1,0),
        vec2(-1,0)
    ];
    for (var i=0; i<4; i++) {
        gridXY.push(lines[i]);
    }
}

function initButtons() {
    currentLabel = document.getElementById("current-step");
    nButton = document.getElementById("nStep");

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
}

function initFileInput() {
    fileInput = document.getElementById('fileInput');
        fileDisplayArea = document.getElementById('fileDisplayArea');

        fileInput.addEventListener('change', function(e) {
            file = fileInput.files[0];
            textType = /text.*/;

            if (file.type.match(textType)) {
                reader = new FileReader();

                reader.onload = function(e) {
                    reset();
                    //fileDisplayArea.innerText = reader.result;
                    allText = '';
                    allText = reader.result;
                    allText = allText.replace(/\s/g, '');
                    allText = allText.replace('/n','')
                    //console.log(allText);

                    p=0
                    for (var i=10; i<20; i++) {
                        for (var j=10; j<20; j++) {
                            grid[i][j] = allText[p];
                            p+=1;
                        }
                    }
                    render();

                    seedFlag = 1;

                    test_with_input();                
                }

                reader.readAsText(file);
            } else {
                fileDisplayArea.innerText = "File not supported!";
            }
        });
}

function test_with_input() {
    render();
    alert("Start")
    textLoc = 0;
    currentStep = 0;
    n = 1;
    errors = 0;
    for (var i=0; i<999; i++) {
        step_it();
        test_for_error();
        //var r = confirm("Continue?");
        /*if (r == false) {
            break;
        }*/
    }
    render();
    alert(errors + " errors found.")
    seedFlag = 0;
}

function test_for_error() {
    p=0
    for (var i=10; i<20; i++) {
        for (var j=10; j<20; j++) {
            if(grid[i][j] != allText[textLoc+p]) {
                errors+=1;
                console.log("Error at step: " + currentStep + " at " + i + " " + j)
                console.log("Model: " + grid[i][j] + " Actual: " + allText[textLoc+p])
                if (errors == 1) {
                    alert("Error at step: " + currentStep + " at (" + i + " " + j + ")" +
                    "\nModel: " + grid[i][j] + " Actual: " + allText[textLoc+p]);
                }
            }
        p+=1;
        }
    }
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
}''