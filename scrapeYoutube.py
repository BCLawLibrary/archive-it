import csv
from pytube import YouTube
from pyexcel_ods3 import save_data
from pyexcel_xlsx import get_data

# get_description() from GitHub user @fartoot
# because pytube's .description doesn't work
# https://github.com/pytube/pytube/issues/1626
def get_description(url):
    yt = YouTube(url)
    for n in range(6):
        try:
            description =  yt.initial_data["engagementPanels"][n]["engagementPanelSectionListRenderer"]["content"]["structuredDescriptionContentRenderer"]["items"][1]["expandableVideoDescriptionBodyRenderer"]["attributedDescriptionBodyText"]["content"]            
            return description
        except:
            continue
    return ""

def get_metadata(url):
    try:
        print(f'Working on: {url}')
        obj = YouTube(url)
        date = f'{obj.publish_date:%b %d, %Y}'
        title = obj.title
        # Archive-It doesn't like newlines in desc.
        # Preserve newlines as "\\n"
        desc = get_description(url).replace("\n", "\\n")
        creator = "Boston College Law School"
        return url, date, title, desc, creator # return tuple
    except:
        print("Video is unavailable...")
        return None

# Input CSV is just a column of YouTube URLs
with open('youtube_urls.csv', 'r') as csvfile:
    urlList = []
    read = csv.reader(csvfile, delimiter=',')
    for i in read:
        urlList.append(i[0])

print('Getting metadata...')
metadataList = [get_metadata(URL) for URL in urlList]
# Filter out Nones
metadataList = [i for i in metadataList if i != None]

print('Writing metadata file...')
with open('youtube_metadata.csv', 'w+', newline='', encoding='utf-8') as csvfile:
    write = csv.writer(csvfile, delimiter=',')
    write.writerow(('url', 'Date', 'Title', 'Description', 'Creator'))
    write.writerows(metadataList)

# Archive-It requires ODS file format
dataCSV = get_data("youtube_metadata.csv")
save_data("youtube_metadata.ods", dataCSV)

print('Complete!')