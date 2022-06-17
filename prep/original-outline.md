# Abstract

It's curious that Python is now the leading language for scientific computing, since pure Python code is not fast and slow code × big data = long wait times. However, most number-crunching in Python is performed by optimized, precompiled libraries: Python only directs the computation, steering it toward the user's intent. As a consequence, the most basic syntax you might learn in an introductory programming class—`if`, `for`, and `while` loops—is not what you should use when dealing with big data. You should use "vectorized" expressions, like slices, broadcasting, and reducers.

This tutorial is an introduction to vectorized array programming. Python beginners are welcome—unfamiliar syntax will be minimized and explained as necessary—because the focus is on _techniques_, rather than language or library features. It is a guided tour through problems with loopy and unloopy solutions, using NumPy and Awkward Array for concreteness, but the techniques can be adapted to any array-oriented setting, such as GPU programming (demo included).

**Tutorial prerequisites:** familiarity programming in any language, or mathematical thinking in general, would be helpful.

**Setup instructions:** none. We'll use cloud-based notebooks with everything preinstalled.

# Outline

Array-oriented programming is a paradigm in its own right, challenging its users to think about problems in a different way. From APL in 1966 to NumPy today, those users are typically scientists analyzing or simulating data. This tutorial focuses on the thought process: all of the problems are to be solved both in an imperative (loopy) way and in a array-oriented (unloopy) way to fully explore this distinction. Also, the problems are all data-centric: analyzing data or performing a simulation, with an eye toward scaling up the problems to big data. Matplotlib will be used for plotting, but all plotting commands will be given (not prerequisites).

The session alternates between expositions of concepts and time-bound problems (about 20 minutes each). At the beginning of the session, in-person participants will be grouped in 3‒4 person teams to work on the problems together, and any online participants can be similarly grouped into Zoom break-out rooms. Each problem will have an optional extension to challenge advanced students/groups.

**Draft outline (subject to adaptation as problems are worked out and pre-tested):**

**0:00‒0:10 (10 min):** Array-oriented programming as a paradigm: APL, SPEAKEASY, IDL, MATLAB, S, R, NumPy. (Showing the keyboard APL used!)

**0:10‒0:30 (20 min):** Arrays (single and multidimensional), element indexing, range slicing, boolean- and integer-array slicing, using text-vectorization as an example. (Powerful concept: element indexing is function application and integer-array slicing is function composition.)

**0:30‒0:40 (10 min):** Applying array-at-a-time (vectorized) functions to an array and multiple arrays (with a word about broadcasting).

**0:40‒1:00 (20 min):** **Exercise (1):** simulating waves in a fluid. I'll explain how to compute a time-step; the problem will be to apply it to all pixels iteratively (with loops and without loops). **Optional extension (1-X):** implement Conway's game of life in a similar way.

**1:00‒1:10 (10 min):** _(break)_

**1:10‒1:30 (20 min):** The "iterate until converged" problem, using a Mandelbrot calculation as an example.

**1:30‒1:50 (20 min):** **Exercise (2):** evaluating a decision tree for many inputs at once (given the tree as an array of indexes pointing to the next nodes, such as what `sklearn.tree.DecisionTreeRegressor` returns). Leaves have to be absorbing states; iteration stops when all inputs reach leaves. **Optional extension (2-X):** instead of the busy-wait, try masking out the inputs that have reached leaves. Which method is faster (for a set of example trees)?

**1:50‒2:00 (10 min):** _(break)_

**2:00‒2:10 (10 min):** **Demo** mixing loopy and unloopy code: computing the Mandelbrot (1) with a Numba kernel for each pixel, (2) parallelized over pixels, and (3) on a GPU.

**2:10‒2:20 (10 min):** Using reducers, with histogram-projection as an example (sum 3D → 2D and 2D → 1D).

**2:20‒2:40 (20 min):** **Exercise (3):** roll your own rolling mean (without `np.convolve` or `pd.DataFrame.rolling`). **Optional extension (3-X):** do it with a non-square kernel (e.g. a Gaussian kernel).

**2:40‒2:50 (10 min):** _(break)_

**2:50‒3:00 (10 min):** Introducing irregularly shaped arrays ("jagged" or "ragged" arrays), using the Awkward Array package: indexing, slicing, and broadcasting with irregular arrays.

**3:00‒3:20 (20 min):** Chicago taxi trip dataset (~GB Parquet file, variable number of trips per taxi and variable length paths per trip): basic exploration, putting techniques into practice (select by fare, by starting point in the city, by starting date, etc.).

**3:20‒3:40 (20 min):** **Reduction exercise (4):** compute path lengths per trip. **Optional extension (4-X):** find the ratio of each with distance "as the crow flies."

**3:40‒4:00 (20 min):** **Bonus exercise (5):** tidy the data (put it in 3rd normal form), resulting in a table of taxis, a table of trips, and a table of positions in paths, all connected by surrogate keys. **Optional extension (5-X):** repeat the calculation of path lengths per trip using "group by" in Pandas.

**Total time: 4 hours.**

All of the exercises are break-out sessions. If in-person, I would walk around the room, checking in on each group as they work. If on Zoom, I would navigate between break-out rooms. (If hybrid, I can do both.) The exposition parts are mini-lectures, using prepared examples, but the students will be encouraged to evaluate them with me so they can change the parameters, explore, and ask questions. The one demo (at **2:00‒2:10**) is also a mini-lecture—whether the students will be able to try it with me depends on whether I manage to get cloud resources with GPUs attached. If not, they'll use mybinder.org without GPUs; they'll only be able to watch.

# Data sources

* The indexing and slicing examples would be drawn from https://github.com/jpivarski-talks/2019-04-08-picscie-numpy/blob/master/03-numpy-skills.ipynb (including the text-vectorization example).
* Mandelbrot with and without loops (including the GPU demo) would be like these performance tests: https://github.com/jpivarski-talks/2019-04-08-picscie-numpy/blob/master/07-coding-fast-and-fast-code.ipynb
* The exercise of walking down a decision tree would come from https://github.com/jpivarski-talks/2019-04-08-picscie-numpy/blob/master/08-day2-homework.ipynb
* "Roll your own rolling mean" and the taxi example for Awkward Arrays are new, but both are straightforward. I've already collected taxi data from https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew but I need to reformat it from tabular JSON into a ragged array in a Parquet file, trimming and compressing it so that it's not much more than a few GB.
