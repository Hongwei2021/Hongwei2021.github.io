**🌍 Overview **

The GTSKG (Geologic Time Scale Knowledge Graph) Project aims to systematically collect all historical versions of the Geologic Time Scale (GTS) published to date, extract their boundary age, and analyze temporal changes in geological period definitions. The processed data is stored in a knowledge graph to facilitate flexible querying and tool development by researchers. This project is an ongoing project.


**🚀 Features **

Version Collection & Boundary Extraction
Aggregates GTS versions from academic publications and extracts boundary ages for geological periods.

Knowledge Graph Storage
Stores data in a structured knowledge graph (RDF format) to enable semantic queries and analysis.


Open Data Sharing
Publishes boundary age datasets as RDF files on GitHub for community use.


Visualization & Analysis
Provides a static website showcasing version comparisons, timeline charts, and statistical summaries.


**📊 Data & Resources **

Dataset: Boundary ages in RDF format ([GitHub Link](https://github.com/Hongwei2021/Hongwei2021.github.io/edit/main))

Dataset：data in excel ([GTSDataWhole.csv])

Static Website: Version summaries and visualizations ([Website Link](https://hongwei2021.github.io/))

Knowledge Graph: RDF/OWL files available upon request.


**🛠️ Technical Implementation **
Python Application Example
A Python script demonstrates how to assign boundary ages to geological units lacking such data.

Workflow:
Input: Geological data without boundary ages (e.g., test dataset from Boucot et al., 2013[[Source](https://www.researchgate.net/publication/268209252_Boucot_et_al_2013_Lithology_Data_Tables_Excel_Spreadsheets/stats)]).

Matching: Align units with the GTSKG.

Assignment: Inherit boundary ages from the closest GTS version.

Output: Enhanced dataset with estimated ages.

Based on the data, the four columns LMU, Period, Stage, and PrimaryReference were selected as evaluation metrics. An algorithm (as shown below) was used to analyze the absolute geological time intervals of samples along with their corresponding uncertainties and version information. After multiple rounds of algorithmic screening, the test results with the highest scores were obtained, yielding 17 versions as the geological time scale version set. Specific algorithmic workflow: Determine whether a geological time concept (GTC) exists (Stage, Period, or a combination with LMU). Prioritize checking Stage before Period. If a GTC is present, store it in the concept variable and proceed to the next step. Phase 1: Determine if the concept appears in the reference versions. Phase 2: Determine if it falls within the range defined by the “difference between the publication date of the competition dataset reference (B) and the publication date of the geological time version (A)”. If within range, check if they are from the same year. If from the same year, the reference version is the output result. If not from the same year, select the version with the smallest difference between A and B.

<img width="2743" height="2853" alt="Code" src="https://github.com/user-attachments/assets/32bea650-708c-4283-9e50-20f47775b13d" />

BGSGT2012 is the most suitable version of the General Geological Time Scale selected by data users. It is appropriate as a version reference for data where version information cannot be determined, and should be applied in conjunction with the intended use and specific objectives of the data.

Cases where version data cannot be determined (select BGSGT2012 for filling) are as follows:
(1) When GTC is stored as concept, it does not exist in the reference geological time scale;
(2) When GTC is a concept, it falls outside the range of B minus A;
(3) No GTC entry exists. Data cleaning primarily includes:
Unifying the LUM column: Lower, Upper, Middle, LM, MU.
Cleaning the country and continent columns for duplicate names and special symbols.
PrimaryReference splits author name information and publication year into two separate columns.
After data cleaning, Pearson correlation coefficients were used to analyze the correlations among features [1]. Missing values in key features were imputed. The figure on the right depicts the correlation matrix among features, where darker colors indicate stronger correlations between corresponding features.
For example, analysis reveals that OldIDNumber and Period exhibit a high degree of correlation, so Period can be populated based on OldIDNumber.
<img width="515" height="422" alt="image" src="https://github.com/user-attachments/assets/7f3e3ec8-79e6-488f-a930-24365963138c" />
Based on the complete dataset, we employed a decision tree to model the full data. Through 10-fold cross-validation, the achieved accuracy reached 96%. The figure on the right depicts the decision tree model.
<img width="835" height="712" alt="image" src="https://github.com/user-attachments/assets/91052cc6-1d1b-4f36-971c-0d4d0b4d2508" />

As shown in the figure below, by applying the t-SNE algorithm to reduce the dimensionality of the original data, a two-dimensional dataset is obtained. Visualizing the Snelling1985 and BGSGT2012 versions reveals that Snelling1985 data points are predominantly clustered in the upper region. For a new test sample, it can be observed that it lies closer to the blue-labeled data points. Therefore, using the k-Nearest Neighbors (KNN) algorithm, it can be classified as belonging to the BGSGT2012 version.
<img width="750" height="457" alt="image" src="https://github.com/user-attachments/assets/3a2d832e-ba83-4c23-b34e-e0f70fb20098" />

**🤝 Contributing **

We welcome contributions!

Report issues or suggest features via GitHub Issues.

Submit pull requests for code/data improvements.

Share missing GTS versions or datasets.



