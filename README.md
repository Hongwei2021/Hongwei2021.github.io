🌍 Overview / 项目概述
The GTSKG (Geologic Time Scale Knowledge Graph) Project aims to systematically collect all historical versions of the Geologic Time Scale (GTS) published to date, extract their boundary age data, and analyze temporal changes in geological period definitions. The processed data is stored in a knowledge graph to facilitate flexible querying and tool development by researchers.
GTSKG（地质年代表知识图谱）项目系统性地收集迄今发布的地质年代表（GTS）所有历史版本，提取其边界年龄数据，分析地质时期定义的时序变化，并以知识图谱形式存储，便于研究者灵活查询与开发工具。

🚀 Features / 核心功能
Version Collection & Boundary Extraction
Aggregates GTS versions from academic publications and extracts boundary ages for geological periods.
版本收集与边界提取
整合学术文献中的地质年代表版本，提取各地质时期的边界年龄数据。

Knowledge Graph Storage
Stores data in a structured knowledge graph (RDF format) to enable semantic queries and analysis.
知识图谱存储
以结构化知识图谱（RDF/OWL格式）存储数据，支持语义查询与分析。

Open Data Sharing
Publishes boundary age datasets as RDF files on GitHub for community use.
开放数据共享
在GitHub以JSON文件共享边界年龄数据集，供社区使用。

Visualization & Analysis
Provides a static website showcasing version comparisons, timeline charts, and statistical summaries.
可视化与分析
静态网站提供版本对比、时间线图表与统计概览。

📊 Data & Resources / 数据与资源
Dataset: Boundary ages in RDF format ([GitHub Link](https://github.com/Hongwei2021/Hongwei2021.github.io/edit/main))

Static Website: Version summaries and visualizations (Website Link)

Knowledge Graph: RDF/OWL files available upon request.

数据集: turtle格式边界年龄数据（GitHub链接）

静态网站: 版本概览与可视化（网站链接）

🛠️ Technical Implementation / 技术实现
Python Application Example
A Python script demonstrates how to assign boundary ages to geological units lacking such data.

Workflow:
Input: Geological data without boundary ages (e.g., test dataset from [Source]).

Matching: Align units with the JOL knowledge graph.

Assignment: Inherit boundary ages from the closest GTS version.

Output: Enhanced dataset with estimated ages.

Python应用案例
演示如何为不含边界年龄的地质单元自动赋值。

流程：
输入: 无边界年龄的地质数据（测试数据集来自[来源]）。

匹配: 与GTSKG对齐地质时间单元。

赋值: 继承最接近GTS版本的边界年龄。

输出: 包含估算年龄的增强数据集。

🔍 How to Use / 使用指南
Clone the repository:

bash
git clone [repository_url]
Install dependencies:

bash
pip install -r requirements.txt
Run the Python script:

bash
python assign_boundary_ages.py --input [input_file] --output [output_file]

🤝 Contributing / 参与贡献
We welcome contributions!

Report issues or suggest features via GitHub Issues.

Submit pull requests for code/data improvements.

Share missing GTS versions or datasets.

欢迎贡献！

通过GitHub Issues提交问题或建议。

提交代码/数据改进的Pull Request。

分享缺失的地质年代表版本或数据集。

