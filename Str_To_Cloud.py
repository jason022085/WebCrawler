import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import numpy as np

class English_Cloud():
    def __init__(self, StrList):
        self.StrList = StrList
        self.cut_str = []

    def no_CH(self, text):
        pattern = "主題:"
        replace = ""
        return re.sub(pattern, replace, text)
    
    def no_space(self, text):
        pattern = '\n    '
        replace = ""
        return re.sub(pattern, replace, text)

    def Cut_Word(self):
        for  i in self.StrList:
            temp_str = self.no_CH(i)
            temp_str = self.no_space(temp_str)
            self.cut_str += temp_str.split("; ")
        # print(self.cut_str)
        return np.array(self.cut_str)

    def Plot_Cloud(self):
        cloud = WordCloud().generate_from_frequencies(frequencies=Counter(self.cut_str))
        plt.imshow(cloud)
        plt.axis("off")
        plt.show()
    
    def WordCloud(self):
        my_array = self.Cut_Word()
        # self.Plot_Cloud()
        # for i in range(len(my_array)):
        #     my_array[i] = my_array[i] + "\n"
        return my_array

# StrList = ["[<strong>主題:\n    </strong>, <strong>Learning</strong>, ' ', <strong>Analytics</strong>, '; Instructional Design; ', <strong>Learning</strong>, ' Strategies; Educational Technology; Computer Assisted Testing; Data Collection; Data Processing']",
#            "[<strong>主題:\n    </strong>, <strong>Learning</strong>, ' ', <strong>Analytics</strong>, '; Reflective Teaching; Metacognition; Decision Making; Instructional Design; Curriculum Development; Open Education; Electronic ', <strong>Learning</strong>, '; ', <strong>Learning</strong>, ' Processes']"]

# df = pd.DataFrame.from_records(Counter(cut_str).most_common(), columns=['Word','Count'])
# print(df)
# out_path = 'D:/' + 'English_Cloud' + '.xlsx'
# out_name = 'D:/English_Cloud.png'
# df.to_excel(out_path, header=False, index=False)


# my_wordcloud.to_file(out_name)