require(academictwitteR)
library(jsonlite)
library(dplyr)
library(feather)
set_bearer()
#> Loading required package: academictwitteR
options(digits=15)

#random dir to save the jsons
tmpdir <- "/Users/dabanto/Desktop/out_tweets_ukr/jsons/"



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

setwd(tmpdir)

files <- list.files(tmpdir, pattern = "^users")
user_content <- jsonlite::read_json(file.path(tmpdir, files[1]))
places_content <- user_content$places
places_content[[1]]

df.all <- data.frame()
for (i in seq_along(files)){
  file.name<-files[[i]]
  df<-read_json(file.name,simplifyVector = FALSE)
  df<-df$places
  df.all<-bind_rows(df.all, df)
}


tweets <- bind_tweets(tmpdir)



df <- df.all
df <- subset(df, lengths(geo) > 0 & names(geo) != "type")
str(df) 



centroid <- lapply(df$geo, function(x) {
  st_coordinates(st_centroid(st_as_sfc(st_bbox(c(xmin=x[[1]], 
                                                 xmax=x[[3]], ymin=x[[2]], ymax=x[[4]])))))
})


dat <- data.frame(df, do.call('rbind', centroid)) 

data_sf = dat %>% st_as_sf(.,coords=c("X","Y"),crs=4326)

data_sf$geo <- NULL

st_write(obj = data_sf, dsn = "/Users/dabanto/Desktop/tweets_dec_22/geo/tws.gpkg")


newtweets<-tweets %>% select(-c(entities,public_metrics,referenced_tweets,attachments, geo, withheld, edit_history_tweet_ids, in_reply_to_user_id)) %>%
  cbind(tweets$public_metrics)


place_id<-list()
for (i in 1:length(tweets$geo$place_id)) {
  if (length(tweets$geo$place_id[[i]])==0) {newval<-c(0,0)}
  else {newval=tweets$geo$place_id[[i]]}
  place_id[[i]]<-newval
}
place_id<-do.call(rbind,place_id)
colnames(place_id)<-c("place_id")
newtweets<-cbind(newtweets,place_id)






data_sf <- rename(data_sf, place_id = id)

data_sf <- data_sf %>% distinct(place_id, .keep_all = TRUE)

df_merge <- merge(x = newtweets, y = data_sf[ , c("place_id", "name", "geometry")], by = "place_id", all.x=TRUE)



st_write(df_merge, "/Users/dabanto/Desktop/tweets_dec_22/geo/output.gpkg")
