// Assignment 1 19T3 COMP1511: CS Paint
// paint.c
//
// This program was written by Xin SUN (z5248104)
// on 22 October 2019
//
// Version 1.0.0 (2019-10-08): Assignment released.

#include <stdio.h>

// Note: you may find the square root function (sqrt) from the math
// library useful for drawing ellipses in Stage 3 and Stage 4.
#include <math.h>

// The dimensions of the canvas (20 rows x 36 columns).
#define N_ROWS 20
#define N_COLS 36

// Shades (assuming your terminal has a black background).
#define BLACK 0
#define WHITE 4

// MORE #defines ADD THEM HERE
#define DARK 1
#define GREY 2
#define LIGHT 3
#define VALID 1
#define INVALID 0

// Provided helper functions:
// Display the canvas.
void displayCanvas(int canvas[N_ROWS][N_COLS]);

// Clear the canvas by setting every pixel to be white.
void clearCanvas(int canvas[N_ROWS][N_COLS]);

// Calculate the distance between two points.
// Note: you will only need this function for the Draw Ellipse command
// in Stages 3 and 4.
double distance(int row1, int col1, int row2, int col2);


// ADD PROTOTYPES OF FUNCTIONS HERE
// Draw straight line form start point to end point with direction
void draw_line(int start_row, int start_col, int length, int direction, int current_color, int canvas[N_ROWS][N_COLS]);

// Fill square from start point by following direction
void fill_square(int start_row, int start_col, int length, int direction, int current_color, int canvas[N_ROWS][N_COLS]);

// Copy parts of painting and paste it in target places in canvas
void copy_paste(int start_row, int start_col, int target_row, int target_col, int length, int direction, int current_color, int canvas[N_ROWS][N_COLS]);

// Draw ellipse with two points and fill colour
void draw_ellipse(int focus1_row, int focus1_col, int focus2_row, int focus2_col, double size, int current_color, int fill, int canvas[N_ROWS][N_COLS]);

// Determine the command has value
// Determine the start point in the canvas
int valid_point(int start_row, int start_col);
// Determine the end point exists in the canvas
int in_canvas(int start_row, int start_col, int length, int direction);
// Detemine the target point in the canvas
int valid_target_point(int target_row, int target_col);
// Determine the target end point exists in the canvas
int target_in_canvas(int target_row, int target_col, int length, int direction);
// Determine a point is in the ellipse
int in_ellipse(int counter_row, int counter_col, int focus1_row, int focus1_col, int focus2_row, int focus2_col, double size);

int main(void) {
    int canvas[N_ROWS][N_COLS];

    clearCanvas(canvas);

    // input variables
    int start_row;
    int start_col;
    int target_row;
    int target_col;
    int length;
    int direction;
    int instruction = -1;
    int current_color = 0;
    int adding_color;
    int checker = 0;
    int focus1_row;
    int focus1_col;
    int focus2_row;
    int focus2_col;
    double size;
    int fill;
    
    // Loop and end by control-D
    while (checker != -1) {
        checker = scanf("%d", &instruction);
        
        // Run draw straight line function
        if (instruction == 1) {
            scanf("%d %d %d %d", &start_row, &start_col, &length, &direction);
            draw_line(start_row, start_col, length, direction, current_color, canvas);
          
          //  Run  fill square function
        } else if (instruction == 2) {
            scanf("%d %d %d %d", &start_row, &start_col, &length, &direction);
            fill_square(start_row, start_col, length, direction, current_color, canvas);
          
          // Change filling colour
        } else if (instruction == 3) {
            scanf("%d", &adding_color);
            current_color = current_color + adding_color;
            if (current_color > 4 || current_color < 0) {
                current_color -= adding_color;
            }
          
          // Copy and move the painting to another places in the canvas
        } else if (instruction == 4) {
            scanf("%d %d %d %d %d %d", &start_row, &start_col, &length, &direction, &target_row, &target_col);
            copy_paste(start_row, start_col, target_row, target_col, length, direction, current_color, canvas);;
        } else if (instruction == 0) {
            scanf("%d %d %d %d %lf %d", &focus1_row, &focus1_col, &focus2_row, &focus2_col, &size, &fill);
            draw_ellipse(focus1_row, focus1_col, focus2_row, focus2_col, size, current_color, fill, canvas);
        }
        
    
    

    }
    // Show painting in canvas
    displayCanvas(canvas);
    
    return 0;
}



// ADD CODE OF FUNCTIONS HERE
// Draw line with colour and direction by scanning start point position and comfirming the end point position in the canvas
void draw_line(int start_row, int start_col, int length, int direction, int current_color, int canvas[N_ROWS][N_COLS]) {
    // Make sure the line can be drew in the canvas
    if (valid_point(start_row, start_col) && in_canvas(start_row, start_col, length, direction)) {
        int counter;
        int counter_row;
        int counter_col;
        
        // Change direction when input length is nagative
        if (length < 0) {
            length = -1 * length;
            direction += 180;
        }
        
        // Get the real direction
        direction = direction % 360;
        
        // Draw line with different directions
        if (direction == 0) {
            counter = start_row;
            while (counter >= start_row - length + 1) {
                canvas[counter][start_col] = current_color;
                counter--;
            }
        } else if (direction == 45) {
            counter_row = start_row;
            counter_col = start_col;
            while (counter_row >= start_row - length + 1 && counter_col <= start_col + length - 1) {
                canvas[counter_row][counter_col] = current_color;
                counter_row--;
                counter_col++;
            }
        } else if (direction == 90) {
            counter = start_col;
            while (counter <= start_col + length - 1) {
                canvas[start_row][counter] = current_color;
                counter++;
            }
        } else if (direction == 135) {
            counter_row = start_row;
            counter_col = start_col;
            while (counter_row <= start_row + length - 1 && counter_col <= start_col + length - 1) {
                canvas[counter_row][counter_col] = current_color;
                counter_row++;
                counter_col++;
            }
        } else if (direction == 180) {
            counter = start_row;
            while (counter <= start_row + length - 1) {
                canvas[counter][start_col] = current_color;
                counter++;
            }
        } else if (direction == 225) {
            counter_row = start_row;
            counter_col = start_col;
            while (counter_row <= start_row + length - 1 && counter_col >= start_col - length + 1) {
                canvas[counter_row][counter_col] = current_color;
                counter_row++;
                counter_col--;
            }
        } else if (direction == 270) {
            counter = start_col;
            while (counter >= start_col - length + 1) {
                canvas[start_row][counter] = current_color;
                counter--;
            }
        } else if (direction == 315) {
            counter_row = start_row;
            counter_col = start_col;
            while (counter_row >= start_row - length + 1 && counter_col >= start_col - length + 1) {
                canvas[counter_row][counter_col] = current_color;
                counter_row--;
                counter_col--;
            }
        }
    }
}


// Draw square with colour and direction by scanning start point position and comfirming the side length in the canvas
void fill_square(int start_row, int start_col, int length, int direction, int current_color, int canvas[N_ROWS][N_COLS]) {
    // Make sure the square can be drew in the canvas
    if (valid_point(start_row, start_col) && in_canvas(start_row, start_col, length, direction)) {
        int counter_row;
        int counter_col;
        int counter;
        // Change direction when input length is nagative
        if (length < 0) {
            length = -1 * length;
            direction += 180;
        }
        // Get the real direction
        direction = direction % 360;
        
        // Draw square with different directions
        if (direction == 0) {
            counter = start_row;
            while (counter >= start_row - length + 1) {
                canvas[counter][start_col] = current_color;
                counter--;
            }
        } else if (direction == 45) {
            counter_row = start_row;
            while (counter_row >= start_row - length + 1) {
                counter_col = start_col;
                while (counter_col <= start_col + length -1 ) {
                    canvas[counter_row][counter_col] = current_color;
                    counter_col++;
                }
                counter_row--;
            }
        } else if (direction == 90) {
            counter = start_col;
            while (counter <= start_col + length - 1) {
                canvas[start_row][counter] = current_color;
                counter++;
            }
        } else if (direction == 135) {       
            counter_row = start_row;
            while (counter_row <= start_row + length - 1) {
                counter_col = start_col;
                while (counter_col <= start_col + length -1) {
                    canvas[counter_row][counter_col] = current_color;
                    counter_col++;
                }
                counter_row++;
            }
        } else if (direction == 180) {
            counter = start_row;
            while (counter <= start_row + length - 1) {
                canvas[counter][start_col] = current_color;
                counter++;
            }
        } else if (direction == 225) {       
            counter_row = start_row;
            while (counter_row <= start_row + length - 1) {
                counter_col = start_col;
                while (counter_col >= start_col - length + 1) {
                    canvas[counter_row][counter_col] = current_color;
                    counter_col--;
                }
                counter_row++;
            }
        } else if (direction == 270) {
            counter = start_col;
            while (counter >= start_col - length + 1) {
                canvas[start_row][counter] = current_color;
                counter--;
            }
        } else if (direction == 315) {       
            counter_row = start_row;
            while (counter_row >= start_row - length + 1) {
                counter_col = start_col;
                while (counter_col >= start_col - length + 1) {
                    canvas[counter_row][counter_col] = current_color;
                    counter_col--;
                }
                counter_row--;
            }
        }
    }
}

// Copy parts of painting drew before
// Paste it to target places in canvas
void copy_paste(int start_row, int start_col, int target_row, int target_col, int length, int direction, int current_color, int canvas[N_ROWS][N_COLS]) {
    // Make sure both intial painting and pasted painting are all existing in canvas
    if (valid_point(start_row, start_col) && in_canvas(start_row, start_col, length, direction) && valid_target_point(target_row, target_col) && target_in_canvas(target_row, target_col, length, direction)) {
        int counter_row;
        int counter_col;
        int counter;
        int i = 0;
        int i_row = 0;
        int i_col = 0;
        // Change direction when input length is nagative
        if (length < 0) {
            length = -1 * length;
            direction += 180;
        }
        // Get the real direction
        direction = direction % 360;
        
        
        if (direction == 0) {
            counter = start_row;
            i = target_row;
            while (counter >= start_row - length + 1 && i >= target_row - length + 1) {
                canvas[i][target_col] = canvas[counter][start_col];
                counter--;
            }
        } else if (direction == 45) {
            counter_row = start_row;
            i_row = target_row;
            while (counter_row >= start_row - length + 1 && i_row >= target_row - length + 1) {
                counter_col = start_col;
                i_col = target_col;
                while (counter_col <= start_col + length -1 && i_col <= target_col + length -1) {
                    canvas[i_row][i_col] = canvas[counter_row][counter_col];
                    counter_col++;
                    i_col++;
                }
                counter_row--;
                i_row--;
            }
        } else if (direction == 90) {
            counter = start_col;
            i = target_row;
            while (counter <= start_col + length - 1 && i <= target_col + length - 1) {
                canvas[target_row][i] = canvas[start_row][counter];
                counter++;
                i++;
            }
        } else if (direction == 135) {       
            counter_row = start_row;
            i_row = target_row;
            while (counter_row <= start_row + length - 1 && i_row <= target_row + length - 1) {
                counter_col = start_col;
                i_col = target_col;
                while (counter_col <= start_col + length - 1 && i_col <= target_col + length - 1) {
                    canvas[i_row][i_col] = canvas[counter_row][counter_col];
                    counter_col++;
                    i_col++;
                }
                counter_row++;
                i_row++;
            }
        } else if (direction == 180) {
            counter = start_row;
            i = target_row;
            while (counter <= start_row + length - 1 && i <= target_row + length - 1) {
                canvas[i][target_col] = canvas[counter][start_col];
                counter++;
                i++;
            }
        } else if (direction == 225) {       
            counter_row = start_row;
            i_row = target_row;
            while (counter_row <= start_row + length - 1 && i_row <= target_row + length - 1) {
                counter_col = start_col;
                i_col = target_col;
                while (counter_col >= start_col - length + 1 && i_col >= target_col - length + 1) {
                    canvas[i_row][i_col] = canvas[counter_row][counter_col];
                    counter_col--;
                    i_col--;
                }
                counter_row++;
                i_row++;
            }
        } else if (direction == 270) {
            counter = start_col;
            i = target_col;
            while (counter >= start_col - length + 1 && i >= target_col - length + 1) {
                canvas[target_row][i] = canvas[start_row][counter];
                counter--;
                i--;
            }
        } else if (direction == 315) {       
            counter_row = start_row;
            i_row = target_row;
            while (counter_row >= start_row - length + 1 && i_row >= target_row - length + 1) {
                counter_col = start_col;
                i_col = target_col;
                while (counter_col >= start_col - length + 1 && i_col >= target_col - length + 1) {
                    canvas[i_row][i_col] = canvas[counter_row][counter_col];
                    counter_col--;
                    i_col--;
                }
                counter_row--;
                i_row--;
            }
        }
    }
}  
 
 
// Draw ellipse by inputing commands       
void draw_ellipse(int focus1_row, int focus1_col, int focus2_row, int focus2_col, double size, int current_color, int fill, int canvas[N_ROWS][N_COLS]) {
    int counter_row = 0;
    while (counter_row < N_ROWS) {
        int counter_col = 0;
        while (counter_col < N_COLS) {
            if (fill != 0 && in_ellipse(counter_row, counter_col, focus1_row, focus1_col, focus2_row, focus2_col, size)) {
                canvas[counter_row][counter_col] = BLACK + current_color;
            }
            counter_col++;
        }
    counter_row++; 
    } 
}                                      

// Make sure the start point is existing in the canvas
int valid_point(int start_row, int start_col) {
    if (start_row >= 0 && start_row <= N_ROWS && start_col >= 0 && start_col <= N_COLS) {
        return VALID;
    } else {
        return INVALID;
    }
}

// Make sure the target point in the canvas
int valid_target_point(int target_row, int target_col) {
    if (target_row >= 0 && target_row <= N_ROWS && target_col >= 0 && target_col <= N_COLS) {
        return VALID;
    } else {
        return INVALID;
    }
}

// Make sure points are in the ellipse
int in_ellipse(int counter_row, int counter_col, int focus1_row, int focus1_col, int focus2_row, int focus2_col, double size) {
    if (distance(focus1_row, focus1_col, counter_row, counter_col) + distance(counter_row, counter_col, focus2_row, focus2_col) <= 2 * size) {
        return VALID;
    } else {
        return INVALID;
    }
}

// Make sure the end point is existing in the canvas
int in_canvas(int start_row, int start_col, int length, int direction) {
    if (length < 0) {
        length = -1 * length;
        direction += 180;
    }
    direction = direction % 360;
    if (direction == 0) {
        if (start_row - length + 1 >= 0) {
            return VALID;
        }
    } else if (direction == 45) {
        if (start_row - length + 1 >= 0 && start_col + length - 1 < N_COLS) {
            return VALID;
        }
    } else if (direction == 90) {
        if (start_col + length - 1 < N_COLS) {
            return VALID;
        }
    } else if (direction == 135) {
        if (start_row + length - 1 < N_ROWS && start_col + length - 1 < N_COLS) {
            return VALID;
        }
    } else if (direction == 180) {
        if (start_row + length - 1 < N_ROWS) {
            return VALID;
        }
    } else if (direction == 225) {
        if (start_row + length - 1 < N_ROWS && start_col - length + 1 >= 0) {
            return VALID;
        }
    } else if (direction == 270) {
        if (start_col - length + 1 >= 0) {
            return VALID;
        }
    } else if (direction == 315) {
        if (start_row - length + 1 >= 0 && start_col - length + 1 >= 0) {
            return VALID;
        }
    }
    return INVALID;
}

// Make sure that after paste the painting is also existing in the canvas
int target_in_canvas(int target_row, int target_col, int length, int direction) {
    if (length < 0) {
        length = -1 * length;
        direction += 180;
    }
    direction = direction % 360;
    if (direction == 0) {
        if (target_row - length + 1 >= 0) {
            return VALID;
        }
    } else if (direction == 45) {
        if (target_row - length + 1 >= 0 && target_col + length - 1 < N_COLS) {
            return VALID;
        }
    } else if (direction == 90) {
        if (target_col + length - 1 < N_COLS) {
            return VALID;
        }
    } else if (direction == 135) {
        if (target_row + length - 1 < N_ROWS && target_col + length - 1 < N_COLS) {
            return VALID;
        }
    } else if (direction == 180) {
        if (target_row + length - 1 < N_ROWS) {
            return VALID;
        }
    } else if (direction == 225) {
        if (target_row + length - 1 < N_ROWS && target_col - length + 1 >= 0) {
            return VALID;
        }
    } else if (direction == 270) {
        if (target_col - length + 1 >= 0) {
            return VALID;
        }
    } else if (direction == 315) {
        if (target_row - length + 1 >= 0 && target_col - length + 1 >= 0) {
            return VALID;
        }
    }
    return INVALID;
}


// Displays the canvas, by printing the integer value stored in
// each element of the 2-dimensional canvas array.
//
// You should not need to change the displayCanvas function.
void displayCanvas(int canvas[N_ROWS][N_COLS]) {
    int row = 0;
    while (row < N_ROWS) {
        int col = 0;
        while (col < N_COLS) {
            printf("%d ", canvas[row][col]);
            col++;
        }
        row++;
        printf("\n");
    }
}


// Sets the entire canvas to be blank, by setting each element in the
// 2-dimensional canvas array to be WHITE (which is #defined at the top
// of the file).
void clearCanvas(int canvas[N_ROWS][N_COLS]) {
    int row = 0;
    while (row < N_ROWS) {
        int col = 0;
        while (col < N_COLS) {
            canvas[row][col] = WHITE;
            col++;
        }
        row++;
    }
}

// Calculate the distance between two points (row1, col1) and (row2, col2).
// Note: you will only need this function for the Draw Ellipse command
// in Stages 3 and 4.
double distance(int row1, int col1, int row2, int col2) {
    int row_dist = row2 - row1;
    int col_dist = col2 - col1;
    return sqrt((row_dist * row_dist) + (col_dist * col_dist));
}
