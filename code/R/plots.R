library(sf)
library(dplyr)
library(ggplot2)
library(forcats)  
library(ggdark)

#read data

df <- st_read("~/idsta/trans_all.gpkg")

df$created_at <- as.Date(df$created_at)


#calculate number of tweets per week
weekly_tweets <- df %>% 
  drop_na(created_at) %>%             
  mutate(daily_tw = floor_date(created_at,unit = "day")) %>% 
  group_by(daily_tw) %>%
  summarise(count = n()) %>%
  complete(daily_tw = seq.Date(min(daily_tw), 
                                   max(daily_tw),by = "day"), fill = list(n = 0))


#create bar plot
ggp <- ggplot(weekly_tweets)  + 
  geom_bar(aes(x=daily_tw, y=count),stat="identity",colour="#006000")+
  scale_x_date(date_breaks = "4 weeks",
               date_labels = "%b-%y") + 
  
  labs(title= "Geolocated tweets for all of Germany related \n to the Russian invasion of Ukraine",
       x="Year-Month",y="Amount of geolocated tweets")+
  dark_theme_gray(base_family = "Fira Sans Condensed Light") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1), plot.title = element_text(size=10, vjust = 3, hjust = 0.5),
        axis.title.y = element_text(size=9, hjust = 0.5, vjust = 4),
        axis.title.x = element_text(size=9, hjust = 0.5, vjust = -3),
        plot.margin = margin(t = 20, r = 20, b = 20, l = 20))



ggsave("~/idsta/graphs/all_tweets_daily.png", plot = ggp, dpi = 300,
       width = 10, height = 8, units = "in", device='png')


#read spatial data contaning the regierungsbezirke borders

spatial <- st_read("~/idsta/shps/NUTS_RG_01M_2021_3035.shp")

spatial <- spatial %>% 
  
  filter(LEVL_CODE == "2" & CNTR_CODE == "DE")


df <- st_transform(df, 4326) # apply transformation to pnts sf
spatial <- st_transform(spatial, 4326)

#locate tweets in regierungsbezirke

pnts <- df %>% mutate(
  intersection = as.integer(st_intersects(geom, spatial))
  , area = if_else(is.na(intersection), '', spatial$NUTS_NAME[intersection])
) 

pnts <- pnts %>%
  filter(!is.na(intersection))

#aggregate tweets per regierungsbezirk
sel <- pnts %>%
  group_by(area) %>%
  dplyr::summarise(count=n())

sel$geom <- NULL

spatial <- rename(spatial, area = NUTS_NAME)

#merge datasets for plot

df_plot <- merge(x = spatial, y = sel[ , c("area", "count")], by = "area", all.x=TRUE)

#set configuration for the plots
black_style  <- structure(
  list(
    bg.color = "black",
    aes.color = c(fill = "grey40", borders = "grey40", 
                  symbols = "grey80", dots = "grey80", 
                  lines = "white", text = "white", 
                  na = "grey30", null = "grey15"),
    aes.palette = list(seq = "YlOrBr", div = "viridis", cat = "Dark2"),
    attr.color = "white",
    panel.label.color = "white",
    panel.label.bg.color = "grey40",
    main.title.color = "white",
    legend.text.size = 0.9,
    legend.title.size = 1.2,
    legend.outside = FALSE
  ),
  style = "black"
)


tmap_options(black_style)

tmap_mode("view")

#plot data

tm <- tm_basemap("OpenStreetMap.DE") + tm_shape(df_plot) +
  tm_polygons(col = "count") +
  tm_text("count", size="AREA", root=5, auto.placement = T) +
  tm_layout(title = "Tweets per Regierungsbezirk",
            legend.position =c("right", "bottom"),
            legend.outside = FALSE,
            inner.margins = c(0.01, 0.01, .12, .34))

tmap_save(tm, "~/idsta/graphs/my_map.html")

#languages

langs <- df %>%
  group_by(lang) %>%
  summarise(n = n()) %>%
  mutate(Freq_langs = n/sum(n)) %>%
  mutate(Perc_langs = Freq_langs*100)

#barplot

p2 <- langs %>% 
  select(lang, n) %>% 
  mutate(lang = fct_reorder(lang, n)) %>% 
  ggplot(aes(lang, n, fill=lang)) +
  geom_col(show.legend = FALSE)+
  geom_text(aes(label = n), size=3)+
  dark_theme_gray(base_family = "Fira Sans Condensed Light", base_size = 14) +
  labs(title= "Number of geolocated tweets per language",
       x="Languages",y="Geolocated tweets") +
  theme(axis.text.x = element_text(vjust = 0), plot.title = element_text(size=10, vjust = 3, hjust = 0.5),
        axis.title.y = element_text(size=9, hjust = 0.5, vjust = 4),
        axis.title.x = element_text(size=9, hjust = 0.5, vjust = -3),
        plot.margin = margin(t = 20, r = 20, b = 20, l = 20)) +
  coord_flip()

p2

ggsave("~/idsta/graphs/langs.png", plot = p2, dpi = 300,
       width = 10, height = 8, units = "in", device='png')



#users per regierungsbezirk

lks <- pnts %>%
  group_by(area) %>%
  summarize(distinct_users = n_distinct(author_id))

lks$geom <- NULL

stats <- merge(x = sel, y = lks[ , c("area", "distinct_users")], by = "area", all.x=TRUE)

stats$tw_by_user <- stats$count/stats$distinct_users

stats_spatial <- merge(x = stats, y = spatial[ , c("area", "geometry")], by = "area", all.x=TRUE)
stats_spatial = st_as_sf(stats_spatial)

#plot

tmap_mode("view")

tm_2 <- tm_shape(stats_spatial) +
  tm_polygons("count", title = "Number of Tweets",
              popup.vars=c( "Number of Tweets: "="count",
                            "Users: "="distinct_users",
                            "Tweets per user (avg): "="tw_by_user")) +
  tm_text(text = "count") +
  tm_view(text.size.variable = TRUE)
tm_2


tmap_save(tm_2, "~/idsta/graphs/plot.html")










