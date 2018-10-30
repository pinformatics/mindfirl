README
================
Gurudev Ilangovan
10/29/2018

# TLDR; What needs to be done:

## Sample 2

### Iteration 1

  - Upload test\_2\_sample\_1.csv and test\_2\_sample\_2.csv and block
    on last name.
  - Verify there are 5 pairs. All of them should be matches.
  - Submit and download report. The output should be
    test\_2\_iter1\_lname\_results.csv

### Iteration 2

  - Upload the test\_2\_iter1\_lname\_results.csv.
  - Block on voter registry number.
  - You should get 1 comparison for empty voter reg number. It is not a
    match.
  - Submit and download report. The output should be
    test\_2\_iter2\_voter\_results.csv

### Iteration 3

  - Upload the test\_2\_iter2\_voter\_results.csv.
  - Block on dob.
  - You should get 3 comparisons. 2 of them are matches and 1 of them
    isn’t.  
  - Submit and download report. The output should be
    test\_2\_iter3\_dob\_results.csv

# Explanation

## Overview

  - The test samples can be found in this directory.
  - The test files are named test\_{test-no}\_sample\_{file-no}.csv.
    File number corresponds to the two files to be uploaded. There is
    also a test\_{test-no}\_sample\_pair.csv that has the groups from
    which the individual files were made.
  - In a way, the pair file represents the ideal grouping but such a
    grouping cannot be achived by exact matching methods.
  - However, we try to get all the groups by repeatedly blocking.
  - The linking procedure with one blocking variable followed by another
    is given here.

## Sample 2

### What happens if you choose different blocking variables?

#### Ideal Group Comparisons (5 group comparisons, 10 pairs)

In these 5 group comparisons, the last group (id-146) alone may not
refer to the same entity. Such compairons cannot be achieved in one
trial using any grouping variable(s) but can only be achieved by
successive compairisons as shown.

ID,voter\_reg\_num,first\_name,last\_name,dob,sex,race <br/>

223\_a,1063209897,BAKRI,ABDEL-AZIZ SR,03/26/1965,M,O <br/>
223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O <br/>
223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O <br/>

333\_a,,MARY DELL,BAKER,04/08/1928,F,W <br/>
333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W <br/>

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W <br/>
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W <br/>

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W <br/>
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W <br/>
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W <br/>

146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W <br/>
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M, <br/>

#### voter\_reg\_num (correct: 3/5 groups, 3/10 pairs | wrong: 1 pair)

223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O <br/>
223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O <br/>

333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W <br/>

333\_a,,MARY DELL,BAKER,04/08/1928,F,W <br/> 358\_a,,W RICHARD,ARCILESI
JR,01/30/1957,M,W <br/>

87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W <br/>
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W <br/>

#### first\_name (correct: 4/5 groups, 4/10 pairs | wrong: 1 pair)

146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W <br/>
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M, <br/>

223\_a,1063209897,BAKRI,ABDEL-AZIZ SR,03/26/1965,M,O <br/>
223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O <br/>

223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O <br/>
333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W <br/>

87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W <br/>
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W <br/>

#### last\_name (correct: 4/5 groups, 5/10 pairs | wrong: 0 pairs)

223\_a,1063209897,BAKRI,ABDEL-AZIZ SR,03/26/1965,M,O <br/>
223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O <br/>
223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O <br/>

333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W <br/>

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W <br/>
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W <br/>

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W <br/>
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W <br/>

### Workflow

#### Iteration 1: Blocking with last name

Let’s say we block with last name. After first round of record linkage
the file will become:

ID,voter\_reg\_num,first\_name,last\_name,dob,sex,race,centroid,group,n
<br/> –groups– <br/> 223\_a,1063209897,BAKRI,ABDEL-AZIZ
SR,03/26/1965,M,O,0,1,3 <br/> 223\_b,1100128569,BAKRI,ABDEL-AZIZ
SR,03/26/1915,M,O,1,1,3 <br/> 223\_bd,1100128569,BAKER,ABDEL-AZIZ
SR,04/08/1982,M,O,0,1,3 <br/>

333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W,1,2,2 <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W,0,2,2 <br/>

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W,1,3,2 <br/>
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W,0,3,2 <br/>

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W,0,4,2 <br/>
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W,1,4,2 <br/>

–singletons– <br/> 146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W,1,5,1
<br/>

146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,,1,6,1 <br/>

333\_a,,MARY DELL,BAKER,04/08/1928,F,W,1,7,1 <br/>

87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W,1,8,1 <br/>

#### Iteration 2: Blocking with voter registry number

Now for the second iteration of record linkage, let’s assume for some
reason we choose voter registry number as our blocking variable. The
already grouped records will not be touched. The centroids alone will be
considered for this round. For instance,

223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O,1,1,3 <br/>
333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W,1,2,2 <br/> 358\_a,,W
RICHARD,ARCILESI JR,01/30/1957,M,W,1,3,2 <br/>
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W,1,4,2 <br/>
146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W,1,5,1 <br/>
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,,1,6,1 <br/> 333\_a,,MARY
DELL,BAKER,04/08/1928,F,W,1,7,1 <br/>
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W,1,8,1 <br/>

We can see that only records 358\_a and 333\_a have the same ID string
(empty). When compared, the user will NOT call it the same becase they
are very different. Hence after this round of rl with voter id, our file
would be the exact same thing:

ID,voter\_reg\_num,first\_name,last\_name,dob,sex,race,centroid,group,n
<br/> –groups– <br/> 223\_a,1063209897,BAKRI,ABDEL-AZIZ
SR,03/26/1965,M,O,0,1,3 <br/> 223\_b,1100128569,BAKRI,ABDEL-AZIZ
SR,03/26/1915,M,O,1,1,3 <br/> 223\_bd,1100128569,BAKER,ABDEL-AZIZ
SR,04/08/1982,M,O,0,1,3 <br/>

333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W,1,2,2 <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W,0,2,2 <br/>

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W,1,3,2 <br/>
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W,0,3,2 <br/>

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W,0,4,2 <br/>
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W,1,4,2 <br/>

–singletons– <br/> 146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W,1,5,1
<br/>

146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,,1,6,1 <br/>

333\_a,,MARY DELL,BAKER,04/08/1928,F,W,1,7,1 <br/>

87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W,1,8,1 <br/>

#### Iteration 3: Blocking with dob

Now we use dob as our blocking variable. Now we get 3 new comparisons
among centroids. If the comparison is positive, we update the

  - centroids (if group \!= min(group), centroid = 0)
  - groups (group = min(group))

As per these rules, we update 333 and 87 but not 146.

333\_a,,MARY DELL,BAKER,04/08/1928,F,W,0,2,1 <br/>
333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W,1,2,2 <br/>

146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W,1,5,1 <br/>
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,,1,6,1 <br/>

87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W,1,4,2 <br/>
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W,0,4,1 <br/>

Finally, we update the n of each group. So the new output file would be:

ID,voter\_reg\_num,first\_name,last\_name,dob,sex,race,centroid,group,n
<br/> –groups– <br/> 223\_a,1063209897,BAKRI,ABDEL-AZIZ
SR,03/26/1965,M,O,0,1,3 <br/> 223\_b,1100128569,BAKRI,ABDEL-AZIZ
SR,03/26/1915,M,O,1,1,3 <br/> 223\_bd,1100128569,BAKER,ABDEL-AZIZ
SR,04/08/1982,M,O,0,1,3 <br/>

333\_a,,MARY DELL,BAKER,04/08/1928,F,W,0,2,3 <br/>
333\_b,1000295504,BAKER,MARY DELL,04/08/1928,F,W,1,2,3 <br/>
333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W,0,2,3 <br/>

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W,1,3,2 <br/>
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W,0,3,2 <br/>

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W,0,4,3 <br/>
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W,1,4,3 <br/>
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W,0,4,3 <br/>

–singletons– <br/> 146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W,1,5,1
<br/> 146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,,1,6,1 <br/>

Even if we had started with out ideal grouping comparisons, we would
have arrived at the same answers. By iteratively blocking, we try to
achieve the same performance (comparison 146’s answer is 0)

## Note

  - pick centroid based on how common it is rather than random?. (87 and
    358)
  - if we block on a new var in an iteration and the matching record in
    another group is not a centroid?
  - singletons to the last

# Unusable groups

## sample 2

### sex (grouping too big)

146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,

223\_a,1063209897,BAKRI,ABDEL-AZIZ SR,03/26/1965,M,O
223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O
223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O

333\_a,,MARY DELL,BAKER,04/08/1928,F,W 333\_b,1000295504,BAKER,MARY
DELL,04/08/1928,F,W 333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W

### race (grouping too big)

146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,

223\_a,1063209897,BAKRI,ABDEL-AZIZ SR,03/26/1965,M,O
223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O
223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O

333\_a,,MARY DELL,BAKER,04/08/1928,F,W 333\_b,1000295504,BAKER,MARY
DELL,04/08/1928,F,W 333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W

### date (correct: 3/5 groups, 4/10 pairs | wrong: 0 pairs)

146\_a,1000153844,KEVIN,RANDALL,08/31/1951,M,W
146\_b,1001039939,KEVIN,PURCELL,08/31/1951,M,

223\_a,1063209897,BAKRI,ABDEL-AZIZ SR,03/26/1965,M,O
223\_b,1100128569,BAKRI,ABDEL-AZIZ SR,03/26/1915,M,O
223\_bd,1100128569,BAKER,ABDEL-AZIZ SR,04/08/1982,M,O

333\_a,,MARY DELL,BAKER,04/08/1928,F,W 333\_b,1000295504,BAKER,MARY
DELL,04/08/1928,F,W 333\_bd,1000295504,BAKER,MARY DELL,04/08/1982,F,W

358\_a,,W RICHARD,ARCILESI JR,01/30/1957,M,W
358\_b,1015248678,WILLIAM,ARCILESI JR,01/30/1917,M,W

87\_a,1075008084,ERNIE,SHORE III,12/17/1959,M,W
87\_b,1705008084,ERNEST,SHORE III,12/17/1959,M,W
87\_bd,1705008084,ERNEST,SHORE,12/17/1959,M,W
