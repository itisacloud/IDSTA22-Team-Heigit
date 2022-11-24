require(academictwitteR)
library(jsonlite)
library(dplyr)
set_bearer()
#> Loading required package: academictwitteR
options(digits=15)

#random dir to save the jsons
tmpdir_test <- academictwitteR:::.gen_random_dir()

#query with the words that we sorted using python
query <- paste0('(','"ukraine" OR "russia" OR "putin" OR "soviet" OR "kremlin" OR "minsk" OR 
                "ukrainian" OR "NATO" OR "luhansk" OR "donetsk" OR "kyiv" OR "kiev" OR "moscow" OR 
                "zelensky" OR "fsb" OR "KGB" OR "Україна" OR "Киев" OR "ФСБ" OR "Россия" OR "КГБ" OR
                "Київ" OR "україни" OR "Росія" OR "кгб" OR "фсб" OR "SlavaUkraini" OR "ukrainian" OR 
                "\\\\U0001F1FA\\\\U0001F1E6" OR "Украина" OR "украины" OR "Donbas" OR "donbas" OR 
                "Донбасс" OR "Донбасс" OR "своихнебросаем"',')', ' has:geo')

#set further parameters, download tweets

get_all_tweets(query,
               start_tweets = "2022-01-01T00:00:00Z",
               end_tweets = "2022-06-30T00:00:00Z",
               file = NULL,
               data_path = tmpdir_test,
               export_query = TRUE,
               is_retweet = FALSE,
               bind_tweets = FALSE,
               verbose = TRUE,
               country = "DE",
               n = 2000)


#create a dataset using the downloaded files where all locations and their respective 
#bounding box are listed

files <- list.files(tmpdir_test, pattern = "^users")
user_content <- jsonlite::read_json(file.path(tmpdir_test, files[1]))
places_content <- user_content$places
places_content[[1]]

df.all <- data.frame()
for (i in seq_along(files)){
  file.name<-files[[i]]
  df<-read_json(file.name,simplifyVector = FALSE)
  df<-df$places
  df.all<-bind_rows(df.all, df)
}


#read all tweets that have been downloaded as a dataframe
tweets <- bind_tweets(tmpdir_test)




