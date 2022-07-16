# "X11, GLX and a math header" -- 07/16/2022

![Nice alt text](../images/pyrimid.png "a pyrimid loaded from an OBJ file")

Quite a bit of progress has been made over the past couple of weeks. ( if you consider getting a pyrimid on the screen "quite a bit of progress" ) Most of my time was spent on the linux platform layer and learning more about the X11/GLX APIs.
Significant things that were built out include:
X11 platfrom layer
OBJ file parser
GL extension loading
A basic math header

This past weekend I learned that gl consumes matrices in column major order. When writing the matrix gen functions, I was using row major since that is what I'm used to. The fix is simply transposing the pre-existing matrices i.e. swapping indicies mat[rowi][coli] becomes mat[coli][rowi].
The 4x4 matrix:
1,  2,  3,  4,
5,  6,  7,  8,
9,  10, 11, 12,
13, 14, 15, 16
Is read by GL as:
1, 5,  9, 13,
2, 6, 10, 14,
3, 7, 11, 15,
4, 8, 12, 16

I know that this is a really short update, Hopefully as more "gamey" things are made, the meat and "intresetingness" of these updates will improve!
Source Code: https://github.com/kroney2/tds.git
