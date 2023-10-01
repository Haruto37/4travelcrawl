from urllib.request import urlopen
import urllib.request
import urllib.parse
import urllib
import lxml.html
import re
import requests
import os

search_place=input('please search place:')#国内
search_place_encode = urllib.parse.quote(search_place)

search_keywords=input('please search keywords:')#大仏
search_keyWord_encode = urllib.parse.quote(search_keywords)


sort_list={1:'departured_at',2:'vote_count',3:'key'}#2
sort_by=int(input(f'please sort by number{sort_list}:'))

number_page=int(input('please nmber of page:'))


root_dict={}#create root_dict


###front page
for page in range(number_page):
    bodyRes = urllib.request.urlopen(f'https://4travel.jp/search/travelogue/dm?order=desc&page={page+1}&sa={search_place_encode}&sk={search_keyWord_encode}&sort={sort_list[sort_by]}')
    bodyHtml = bodyRes.read()
    root = lxml.html.fromstring(bodyHtml.decode('utf-8',errors='replace'))
    title_path = root.xpath("//a[@class='ico_travelogue']")


    #create root_list of "deep page path" gotten from front page path with "xpath" method
    root_list=[]
    for path in title_path:
        root_list.append(path.get('href'))


    #insert created root_list as page_(page+1) into root_dict 
    root_dict[f'page_{page+1}']=root_list
    

###completed root_dict is type of "dict" contained root_list as page_(page+1) each line


###deep page
image_dict={}#create image_dict
s_dict={}#create sentence_dict


for page in range(number_page):

    image_list=[]
    s_list=[]
    #extract root_list from root_dict 
    root_dict_list=root_dict[f'page_{page+1}']
    for root_list_n in root_dict_list:

        bodyRes = urllib.request.urlopen(root_list_n)
        bodyHtml = bodyRes.read()
        root = lxml.html.fromstring(bodyHtml.decode('utf-8',errors='replace'))


        #create image_list gotten from front root_list in root_dict with "xpath" method
        image_path = root.xpath("//a[@class='swipebox']")
        
        for path in image_path:
            image_list.append(path.get('href'))


        #create s_list gotten from front root_list in root_dict with "xpath" method
        sentence_path = root.xpath("//p[@class='contentsDescription']")
        
        for path in sentence_path:
            s_list.append(''.join(re.findall('[一-龥ぁ-んァ-ンー々]+|[0-9]+' ,path.text_content())))
    

    image_dict[f'page_{page+1}']=image_list
    #insert created image_list as page_(page+1) into root_dict 
    s_dict[f'page_{page+1}']=s_list
    #insert created s_list as page_(page+1) into root_dict 


###completed image_dict and s_dict is type of "dict" contained image_list or s_list as page_(page+1) each line


#this is current directory
dir_=__file__
dir_current=os.path.dirname(dir_)
#print(root_dict)
#print(s_dict)
#print(image_dict)
for page in range(number_page):


    #extract root_list from root_dict 
    image_dict_list=image_dict[f'page_{page+1}']


    #create "image_file(page+1)" in current directory each "for" method
    dir_path=f'{dir_current}\image_file{page+1}'
    os.mkdir(dir_path)


    for im_dict_page in range(len(image_dict[f'page_{page+1}'])):###length of image_list in image_dict 

        #save extracted "image" from imgae_list in image_dict as "image(page+1)_(im_dict_page).jpg" in set directory
        file_name=f'{dir_path}\imgae{page+1}_{im_dict_page}.jpg'
        responce=requests.get(image_dict_list[im_dict_page])
        image_content=responce.content

        with open(file_name,'wb') as f:
            f.write(image_content)