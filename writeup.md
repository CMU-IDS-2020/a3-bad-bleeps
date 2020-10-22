# How To Get Away With Murder: Data Edition

![A screenshot of your application. Could be a GIF.](screenshot.png)

TODO: Short abstract describing the main goals and how you achieved them.

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 

In this project, we asked the questions: what types of crime do chicago police prioritize? and do all police districts have similar arrest rates? The goal of this project was to help users visualize how the district and type of crime affect arrest rates in Chicago, so we created visualizations that help users compare over different types and districts through time. From these, they can see districts that have higher or lower than average arrest rates, or crimes which crimes are treated as the worst offenses in chicago.

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?
We chose our particular visual encodings and interaction techniques by first sketching out different ideas for visualizations that we had. Starting from a bird's eye view, we asked ourselves what information did we want to see at a high level. 

For our question about analyzing types of crime and crime frequencies, we first decided on using an area graph to show the frequencies of different types of crime over time. 
When considering how to encode the type of crime, we decided on using color as it works easily for categorical data and specifically data with many categories such as the type of crime; however, with data that had so many categories such as the type of crime, it became difficult to read a legend that had so many rows for all the different types of crime.
To combat this, we elected to use the tooltip to highlight the specific primary type that the user had currently highlighted in addition to the color to provide further information that reinforced the association between color and crime type.
We repeated this when visualizing changes in frequency and arrest rates over time, where we used the color and tooltip again to convey which primary type of crime the user was currently interacting with. Additionally, we emphasized the current type the user was looking at by making the selection's line bigger and lowering the opacity of all other lines.
We decided to make the opacity close to 0 but not equal to 0 so that the user would still be able to see the other lines and know where to hover in order to focus on a specific line.

Our other question tackled the location of crime and arrest rates within districts. For this visualization, we first mapped the x and y coordinates of all crimes so that the user could have a form of a heat map that indicated where they could zoom in to see more of the data.
Because the axes of the data were geographic in nature, we decided to go with a brush selection to function as a sort of mangifying glass for the data and allow users to take a closer peek at the information in front of them. Because geographic boundaries aren't discrete in a manner that crime types are, using a brush selection helps the user easily pan around the data.
We originally thought of using a histogram to convey the frequencies of crimes per district, but this removed the geographic elements of the x and y coordinates as a histogram would just have the district on one axis. Instead, we decided to keep the x and y coordinates for the zoomed in view of the data, and instead used the size of the dots at the x and y coordinates to communicate frequency.
Using size also helped visualize relative differences between nearby locations. 

The final visualization relied on examining the different arrest rates per district to see if specific districts were being faced with higher policing rates. Because the visualization was centered around the different districts, we decided to use a map to highlight the different districts so the user could get an idea of where each district was located.
We then allowed the user to select the district, which would then highlight the crime frequency and arrest rates for that district over time. While we were creating this visualization, we noticed that it was difficult to discern how a particular district compared to the other districts, and combated this by adding an average line for crime frequency and arrest rate so that viewers would be able to see any significant differences between the selected district and the average across all districts.
Additionally, we considered the interactivity of the graphs showing the rates/frequencies over time. If a user wanted to be able to select the district with the highest arrest rates over time, they would not have been able to do that if they did not first select the district on the map, which could be confusing. Thus, we added an interaction where the line can also be selected by clicking on it similar to clicking on a specific district.

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?


Workwas split by topic; one team member focused more on visualizations for crime types, and another focuesd more on visualizations for crimes by district. We also split the ML portion so that one member worked on building and training models while the other implemented in the app and allowed it to make predictions on information that users input.

 This project built off of one that was done for HW2, so we had already explored the data and saw that we wanted to create more visualizations that explored the relationships between the type of crime, the district that it took place in, and crime and arrest rates. The most time-consuming part of development was deciding how to best group together visualizations for one topic into a cohesive display and trying to create the visualizations that matched our plans. After we determined questions to ask from the EDA, it took a few days to figure out how to best store and process the data as well as familiarize ourselves with altair and streamlit by making some basic visualizations that we didn't end up including in our final app. Each visualization took 3-4 hours to create. It also took 1-2 days to familiarize ourselves with scikit-learn and use to create relevant machine learning models.

