Prosper Loan Exploratory Data Analysis by Mitchell Barnes-Wallace
=================================================================





# Univariate Plots Section


![plot of chunk Univariate_Plots1](figure/Univariate_Plots1-1.png)

The Prosper Loan Data contains the data from the Peer to Peer (p2p) lending site Prosper. This dataset contains a total of 81 variables with over 113,000 observances. For this analysis I will explore at the following 11 variables from the data set, with loans issued after July 2009, as all loans issued after July were structured under new guidelines. 

* ProsperRating: Rating of the loan when the listing was created. Values vary from HR (worst) - AA (best);
* ProsperScore:The score ranges from 1-11, with 11 being the best, or lowest risk score;
* LoanOriginalAmount: The origination amount of the loan;
* LoanOriginationQuarter: The quarter the loan originated;
* IncomeRange: The income range of the borrower at the time the listing was created;
* IncomeVerifiable: The borrower indicated they have the required documentation to support their income;
* EstimatedReturn: Estimated return for the lender(s) is the difference between the Estimated Effective Yield and the Estimated Loss Rate.
* Investors: The number of investors that funded the loan.
* InvestmentFromFriendsAmount: Dollar amount of investments that were made by friends.



![plot of chunk Univariate_Plots2](figure/Univariate_Plots2-1.png)

The ratings are distributed normally, with a majority of the listings fall between A-D ratings and a select few listings awarded a AA rating. 

![plot of chunk Univariate_Plots3](figure/Univariate_Plots3-1.png)

Similar to the Propser Rating, the the Prosper Score is distributed normally. Though as too be expected the distribution isn't quite the same, as there are more score levels and they measure slightly different aspects of the listing. 

![plot of chunk Univariate_Plots4](figure/Univariate_Plots4-1.png)

The Loan Origional Amount is skwewed right with a majority of the listings containing loans less than $10,000. There are peaks on this graph at round values. \$5,000, \$10,000 \$15,000 etc. This should be expected as most people might request \$5,000 as opposed to say, \$5,340. 

![plot of chunk Univariate_Plots5](figure/Univariate_Plots5-1.png)

Following the restart of the Prosper website, the number of Lisitings issued per quarter, grows gradually until Q4 of 2012, reaching a local minimum in Q1 of 2013.

![plot of chunk Univariate_Plots6](figure/Univariate_Plots6-1.png)

The plot of Income Ranges doesn't quite fit a normal distribution. With most of the lisings containing lendees whose incomes fall between \$25,000 and \$99,999. There are also surprisingly more people that are "Not Employed" than people that reported an income of \$0.  

![plot of chunk Univariate_Plots7](figure/Univariate_Plots7-1.png)

The vast majority of lisings had verifiable income, with over 60,000 listings verified as opposed to under 5,000 unable to be verified. Most people looking for loans on a Peer 2 Peer sight might be more likely to have unverifiable income, otherwise they would have gone to a more conventional lender. Over 75% of the lisings here have verifiable income, which is likely a lower percentage than you might see at a traditional lender. 

![plot of chunk Univariate_Plots8](figure/Univariate_Plots8-1.png)

The estimated return of the for this data set takes a bimodal distribution, with the first peak around 7%, second around 12% and additionally a third peak, that is just outside the center of the graph, at around 15%. 

![plot of chunk Univariate_Plots9](figure/Univariate_Plots9-1.png)

The graph of the Number of Investors is skewed right with most of the data points lying below 100 investors. A large number of the listings have 1 investor, which matches what might be expected. The mean of this distribution is just over 73, and the median for this graph is 36.  

![plot of chunk Univariate_Plots10](figure/Univariate_Plots10-1.png)

Looking at the investment from Friends Amount, in the graph on the left, most of the data points lie at 0, and completely overshadows all other buckets with a value close to 70,000 listings. The graph on the right shows the distribution with the zeros removed. Both of these graphs are right skewed with a vast majority of listings not recieving any funding from friends. Loaning money to friends can cause tension in the friendship, which might disuade many people from loaning to friends. 

# Univariate Analysis

### What is the structure of your dataset?
This dataset contains a total of 81 variables with over 113,000 observances. Each line of data contains information that describes a specific loan listed on the Prosper website. At core of it, the data contains basic information about the loan, including how much the loan is for, the term of the loan and the loan origionation date. The dataset also includes additional information that provides more detailed information about the lendee, including where they live, their credit score, etc. 

### What is/are the main feature(s) of interest in your dataset?

My main feature of interest is in the lending patterns between friends on this site. Mostly, does a lower credit score make it more or less likely that a friend will provide the funds. 

### What other features in the dataset do you think will help support your investigation into your feature(s) of interest?

Additional features in the dataset that will support the investigation include, the more descripitive information about the lendee, including their salary range, whether or not their income is verifiable. 

### Did you create any new variables from existing variables in the dataset?

I created two variables to add to this dataset that will be used in the bivariate analysis. This first is FriendInvested, a boolean that is True when the listing is funded by a friend, and False when no friends fund the listing. The second variable,FriendsPercentFunded, produces a percentage for the lisings funds invested by friends. 

### Of the features you investigated, were there any unusual distributions? Did you perform any operations on the data to tidy, adjust, or change the form of the data? If so, why did you do this?

Initially, when looking at the income range graph, it initially looked fine as it was normally distributed. However I noticed that I had to do some manipulation with the levels of some of the factored variables, like the income range variable, was ordered alphabetically, and not by the appropriate order. 

# Bivariate Plots Section

![plot of chunk Bivariate_Plots](figure/Bivariate_Plots-1.png)

In the Income Range graph with the Income Verifiable overlayed, most of the income unverifiable lie in the middle range from \$25,000 - \$74,000. Which matches that portion having the largest number of listings overall. Additionally, the lendees that are not employed all have unverifiable income as they don't have income to verify. 

![plot of chunk Bivariate_Plots2](figure/Bivariate_Plots2-1.png)

Introducing the Income Verifiable variable to the Loan Origional Ammount reveals results matching expectations. Most of the lendees without verifiable income have listings below $10,000, which matches those with verifiable income. The mean of those with verifiable income is greater than those without verifiable income. When looking at the medians of the two populations (solid lines), the difference becomes greater, likely due to the outliers in both populations. The median for verifiable income borrowers is approximentally \$7,000 while the median for the population of income unverifiable borrowers is approximentally \$4,000.


![plot of chunk Bivariate_Plots10](figure/Bivariate_Plots10-1.png)

The percent funded by friends amount, excluding those that had $0 invested from friends, is skewed right, with the median of the graph sitting to  the left of the mean. Most of the lendees had fewer than 5% of their total lising invested in by friends. Additionally, there is one data point where friends invested more than 100% of the total listing, we will look more at this point later. 



![plot of chunk Bivariate_Plots4](figure/Bivariate_Plots4-1.png)

For the Loan Oringional Ammount, when compared across income range, the distributions are all skewed right, with the averages following an interesting trend. Lendees from the [\$25,000,\$49,999] up to the \$100,000+ group, increases with increasing income range. After that, the mean of the \$0 income range followings the [\$25,000,\$49,999], which counters the trend discoverd at the higher income levels. 

![plot of chunk Bivariate_Plots5](figure/Bivariate_Plots5-1.png)

For the Estimated Return, the Prosper Rating appears to play an impact in the moving the average return from the investment. For the highest rated lisings, the estimated return is the lowest, with the lising not rated and the E rated lisings having nearly the same estimated return for the highest on the set. For investors, a lower rated loan carries more risk, as there is a higher likelyhood that the borrower will default on their loan, then for a higher rated borrower. This causes the lender to charge a higher interest rate, which brings up the Estimated Return on the loan.

# Bivariate Analysis

### Talk about some of the relationships you observed in this part of the investigation. How did the feature(s) of interest vary with other features in the dataset?

Investigating the income verifiable variable turned up some interesting results. Income verifiable doesn't seem to really vary all that much across income ranges. The not-employeed group is 99.3% unverifiable income and the \$0 range has a similarily high percentage at 84.7%, while all other ranges have comparable percentages:

Not employed -> 99.3%
\$0 -> 84.7%
\$1-24,999 -> 17.9%
\$25,000-49,999 ->  9.27%
\$50,000-74,999 -> 6.33%
\$75,000-99,999 -> 5.77%
\$100,000+ -> 7.63%

Verifiable income also appears to influence the origional loan amount. The average origional loan amount for unverifiable income is \$6,577.24, while the average origional loan amount for verifiable income is \$8,929.95. For lisitings that were invested in by the borrowers friends, the median percent funded by friends is 3%, while the mean percent funded is 12%, only for the borrowers with friends invested in their lisings. One of the lisings was actually invested over 100% of the asking amount. For this listing is in the highest income range and a Military Officer, this may be a mistake in the system. 

Looking at the Income Range's impact on the origional loan amount. 
<table>
 <thead>
  <tr>
   <th style="text-align:left;"> Income Range </th>
   <th style="text-align:left;"> Loan Original Amount </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Not employed </td>
   <td style="text-align:left;"> $5,272.15 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> $0 </td>
   <td style="text-align:left;"> $6,061.87 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> $1-24,999 </td>
   <td style="text-align:left;"> $4,289.88 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> $25,000-49,999 </td>
   <td style="text-align:left;"> $6,442.29 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> $50,000-74,999 </td>
   <td style="text-align:left;"> $9,051.47 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> $75,000-99,999 </td>
   <td style="text-align:left;"> $10,706.23 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> $100,000+ </td>
   <td style="text-align:left;"> $13,385.92 </td>
  </tr>
</tbody>
</table>
The average Original Loan Amount increases generally from the lowest income range up to the largest income range. However, there is a dip at the \$1-24,999 income range. The relationship between Estimated Return and Prosper Rating also displayed some interesting results. The best rated borrowers had the lowest median return and the worst rated borrowers had the highest median return.

### Did you observe any interesting relationships between the other features (not the main feature(s) of interest)?

In looking at the Friends Invested Number, I found it difficult to make any meaningful graphs or conclusions from the population as a whole, but rather had to drill down to look at only the listings that recieved any investments from friends. This yielded the expected result most of the lisings weren't nearly fuly funded. The most interesting discovery I made personally, was the percentage return estimate across different Prosper Scores. The result was certianly logical, but when I initially looked at the data, I expected a different result, with an inverse of the median trends present. 

### What was the strongest relationship you found?

Two of the stronger relationships found were between the median Estimated Return and Prosper Rating, and the average origional lising amount delta between the Income Verifiable and Income Inverifiable, with a mean difference of nearly $2,500, there appears to be some realtionship between Income Verifiability and the Origional Lising Amount. 


# Multivariate Plots Section

![plot of chunk Multivariate_Plots](figure/Multivariate_Plots-1.png)

In the first multivariate plot, I looked at the distributions of the origional loan amount across the different income ranges, split but Income verifiability. In this plot the data follows an interesting pattern. As the income range increases, the distribution of the graph moves from skewed right, to almost uniform at the highest level of income. Digging a little deeper into the medians accross income verifiablity, I found that at the lower ends of the income ranges, there median for the borrowers that had unverifiable income was greater than those with verifiable income, ie (\$4,000 v \$2,000), at the \$1-24,999 income range the two medians are equavlent and from there the median origional loan amount for the verifiable borrowers distances itself from the inverifiable borrowers with the highest earners with verifiable income having a median original loan amount almost double that of the unverifiable. This relationship is shown in the plot below. 

![plot of chunk Multivariate_Plots2](figure/Multivariate_Plots2-1.png)

![plot of chunk Multivariate_Plots3](figure/Multivariate_Plots3-1.png)

Of the borrowers recieving investment from friends, the income verifiablity does appear to play some role in the percentage funded by the borrower's friends. The median percent invested in the verified borrower is 2.7% while those without verified income have friends investing in more than twice that amount at 6.1%.

![plot of chunk Multivariate_Plots4](figure/Multivariate_Plots4-1.png)

When looking at the graphs comparing the estimated return across both income ranges and prosper ratings, I used box plots because I felt they gave us a good understanding of the spread of the data here. For most of the rating levels, the interquartile range remainings approximentally the same. We again see a change in the Not Employed and \$0 Income Ranges. While the IQR remaings approxientally the same, the median at each Rating Level moves to the left as the income range increases (at higher prosper scores), and at lower prosper scores the median moves to the right as the income levels increase. 

# Multivariate Analysis

### Talk about some of the relationships you observed in this part of the investigation. Were there features that strengthened each other in terms of looking at your feature(s) of interest?

Of the features I looked at, income verifiability seemed to strengthen the friends investment percentage the most. Only looking at the invements where friends invested in the loan, which certainly isn't to the most robust method of studying this trend, the average friend investment percentage increased for those without verifiable income. Using percentage here, as opposed to dollars invested, helped to bring into context the investment of the friends (ie if someone only asked for \$2,000 and a friend invested half, that would carry the same weight as a friend investing \$1,000 in a \$4,000 loan.) Income verifiability also played a role in the origional loan amount across income ranges. While, in general, the median loan amount across income ranges increased for both the income verifiable and the income inverifiable, the relationship between these two amounts changed. The median income for the inverifiable starts out as greater than for the income verifiable, but as the income range increases, the income verifiable's median loan amount surpases and then almost doubles the median income for the income inverifiable. Lastly, I looked at the estimated return across income ranges and prosers score. In general, it appeared that the income range had no major impact in the estimated return of the listing, but rather the prosper rating appeared to make a much bigger. 

### Were there any interesting or surprising interactions between features?

The most interesting relationship I found was in the percent funded by friends across income verifiability. While intitially I thought that friends might be less inclined to invest in their friends the more red flags pop up in a listing (ie Income Inverifiable), it appears at least for this variable, friends invest at a higher percentage for the income inverifiable. With the average percent invested for the income verifiable also being greater than the income verifiable. (17.8% and 11.2% respectively)

------

# Final Plots and Summary

### Plot One
![plot of chunk Plot_One](figure/Plot_One-1.png)

### Description One

Income range was an area I wanted to investigate further in this study. Looking at the Median Origional Loan Amount across the income range, factoring in the verifiability of the borrowers income, brought out an interesting trend. For those in the lower income ranges (i.e. less than \$24,999) the median Origional Loan Amount was greater for those with unverifiable income. As the income range increased, the median incomes for both groups increase, with the Income verifiable group increasing at a much faster rate, almost doubling the median origional loan amount at the highest income range (\$100,000). The general trend of the median loan origional amount increasing as the income ranges increases makes sense. The more someone makes, the more money they are comfortable borrowing. The trend found with the medians across the Verifiable Income groups follows similar logic but in the reverse direction. Those with verifiable income have a better credit score, and are likely better off finacially. At the lower income ranges, people without verifiable income might need more money in order to meet their finacial needs at the moment. Another possible expalation, is that at the lower income ranges the groups are smaller, which allows for more variance, and in the middle income ranges (\$25,000-49,000 & \$50,000 - 74,999), the grops are big enough to bring the median more towards the middle of the overall population, and we see similar potential error at higher income ranges as we do at lower income ranges, just in the reverse. This theory, however, seems pretty far fetched. 

### Plot Two
![plot of chunk Plot_Two](figure/Plot_Two-1.png)

### Description Two

In investigating the investment percentage of friends across different propser ratings, between the two income verifiability groups yields interesting results as well. For those without verifiable income, the mean investment percentage is greater than those with verifiable income for all of the Prosper Ratings other than the E rating. For those with an inverifiable income, they likely needed to rely more on friends in order to get the funds needed for their loan. This group, is however not a true sample, as it is selected only from people that recieved money from friends at all. A vast majority of lisings did not recieve any money from friends at all. In this group we see the highest mean invest percentages of the incoem inverfiable on the edges, for the best rated and the worst rated. For the income verifiable the is a general downward trend from the worst rated (HR) up to the best rated (AA). Following to trains of logic here. For the better rated lisings, the borrower is less likely to need a friends help in funding their loan. But, for the income inverifiable, the may need their friends help in order to reach their full needed loan as other lenders might seem them as higher risk. This data does provide some interesting results, income range may be able to provide further insight into this trend. 

### Plot Three
![plot of chunk Plot_Three](figure/Plot_Three-1.png)

### Description Three

Lastly, I wanted to compare the two groups, those with friends invested, and those without. Initially, I thought that for those who did not need friends investment would have a higher estimated reutrn, while those with friens invested would have a lower median estimated return. For most of the gorups, the estimated return is actually higher for the loans that have friends investment. The lowest rating group HR has a much higher estimated return for the loans without friends invested than with friends invested, this is the same as the B Rating, the A rating is practically the same percetage of estiamted return. For the carrer lenders, it would make sense for them to make investments in a lot of low risk, low return loans. While with friends, the loans might be higher risk, but the return is higher and the friends might feel more comfortable lending because they know the person. For the highest risk loans, the median return is actually lower for the non-friend invested group. For this group, the non-friends might only be comfortable with investing in loans at this rating with high returns, as it is nearly the highest estimated return of any rating group, and that would move the median towards the higher side. 

-----

# Reflection

This dataset was large and pretty intimidating at first. It took me a good amount of time just looking at all of the variables present and figuring out which variables to investigate. I found the Income Verifiable variable and the Friend Investment amount most interesting to investigate, as both provided a distinct result and I wasn't quite sure how these variables would influence the other variables in this dataset. There were a few issues I ran into, including plot scaling issues and determining which plots would most effectively display the data I was presenting. There is a ton of future work that can still be done in investigating this dataset, including investigating the borrowers profession influence on the loan origional amount, prosper rating, etc. I found most of the information displayed in my final plots surprising. My initial assumptions here with these plots were proven incorrect, but it did provide some useful insight to me on the innerworkings of the P2P loan industy. 
