
CREATE TABLE `twigrapher`.`AllFromTwitterAPI` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `request_type` TEXT NOT NULL,
  `json_col` LONGTEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `extracted` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE
);



CREATE TABLE tweets (
  
  `added_at` DATETIME DEFAULT CURRENT_TIMESTAMP,

  `id_str` BIGINT NOT NULL PRIMARY KEY,
  `full_text` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL,

  `source` TEXT,
  `in_reply_to_status_id_str` BIGINT,
  `in_reply_to_user_id_str` BIGINT,
  `in_reply_to_screen_name` TEXT,

  `is_quote_status` TINYINT,
  `quoted_status_id_str` BIGINT,
  `quoted_status` TEXT,

  `favorited` TINYINT,
  `retweeted` TINYINT,
  `retweet_count` INT,
  `favorite_count` INT,

  `possibly_sensitive` TINYINT,
  `filter_level` TEXT,

  `lang` TEXT,




  `user_id_str` BIGINT,
  `user_name` TEXT,
  `user_screen_name` TEXT,
  `user_location` TEXT,
  `user_url` TEXT,
  `user_description` TEXT,
  `user_protected` TINYINT,
  `user_verified` TINYINT,
  `user_followers_count` INT,
  `user_friends_count` INT,
  `user_listed_count` INT,
  `user_favourites_count` INT,
  `user_statuses_count` INT,
  `user_created_at` DATETIME,
  `user_profile_banner_url` TEXT,
  `user_profile_image_url_https` TEXT,
  `user_withheld_in_countries` TEXT,





  `place_place_type` TEXT,
  `place_name` TEXT,
  `place_full_name` TEXT,
  `place_country_code` TEXT,
  `place_country` TEXT,
  `place_bounding_box_coordinates_1Long` DOUBLE,
  `place_bounding_box_coordinates_1Lat` DOUBLE,
  `place_bounding_box_coordinates_2Long` DOUBLE,
  `place_bounding_box_coordinates_2Lat` DOUBLE,
  `place_bounding_box_coordinates_3Long` DOUBLE,
  `place_bounding_box_coordinates_3Lat` DOUBLE,
  `place_bounding_box_coordinates_4Long` DOUBLE,
  `place_bounding_box_coordinates_4Lat` DOUBLE,
  `place_bounding_box_type` TEXT,
  
  `coordinates_type` TEXT,
  `coordinates_coordinates_Long` DOUBLE,
  `coordinates_coordinates_Lat` DOUBLE,





  `entities_hashtags0_indices_start` INT,
  `entities_hashtags0_indices_end` INT,
  `entities_hashtags0_text` TEXT,

  `entities_hashtags1_indices_start` INT,
  `entities_hashtags1_indices_end` INT,
  `entities_hashtags1_text` TEXT,

  `entities_hashtags2_indices_start` INT,
  `entities_hashtags2_indices_end` INT,
  `entities_hashtags2_text` TEXT,

  `entities_hashtags3_indices_start` INT,
  `entities_hashtags3_indices_end` INT,
  `entities_hashtags3_text` TEXT,

  `entities_hashtags4_indices_start` INT,
  `entities_hashtags4_indices_end` INT,
  `entities_hashtags4_text` TEXT,

  `entities_hashtags5_indices_start` INT,
  `entities_hashtags5_indices_end` INT,
  `entities_hashtags5_text` TEXT,

  `entities_hashtags6_indices_start` INT,
  `entities_hashtags6_indices_end` INT,
  `entities_hashtags6_text` TEXT,

  `entities_hashtags7_indices_start` INT,
  `entities_hashtags7_indices_end` INT,
  `entities_hashtags7_text` TEXT,


  `entities_media0_display_url` TEXT,
  `entities_media0_expanded_url` TEXT,
  `entities_media0_id_str` BIGINT,
  `entities_media0_indices_start` INT,
  `entities_media0_indices_end` INT,
  `entities_media0_media_url` TEXT,
  `entities_media0_media_url_https` TEXT,
  `entities_media0_type` TEXT,
  `entities_media0_url` TEXT,

  `entities_media1_display_url` TEXT,
  `entities_media1_expanded_url` TEXT,
  `entities_media1_id_str` BIGINT,
  `entities_media1_indices_start` INT,
  `entities_media1_indices_end` INT,
  `entities_media1_media_url` TEXT,
  `entities_media1_media_url_https` TEXT,
  `entities_media1_type` TEXT,
  `entities_media1_url` TEXT,

  `entities_media2_display_url` TEXT,
  `entities_media2_expanded_url` TEXT,
  `entities_media2_id_str` BIGINT,
  `entities_media2_indices_start` INT,
  `entities_media2_indices_end` INT,
  `entities_media2_media_url` TEXT,
  `entities_media2_media_url_https` TEXT,
  `entities_media2_type` TEXT,
  `entities_media2_url` TEXT,

  `entities_media3_display_url` TEXT,
  `entities_media3_expanded_url` TEXT,
  `entities_media3_id_str` BIGINT,
  `entities_media3_indices_start` INT,
  `entities_media3_indices_end` INT,
  `entities_media3_media_url` TEXT,
  `entities_media3_media_url_https` TEXT,
  `entities_media3_type` TEXT,
  `entities_media3_url` TEXT,
  


  `entities_urls0_indices_start` INT,
  `entities_urls0_indices_end` INT,
  `entities_urls0_url` TEXT,
  `entities_urls0_display_url` TEXT,
  `entities_urls0_expanded_url` TEXT,

  `entities_urls1_indices_start` INT,
  `entities_urls1_indices_end` INT,
  `entities_urls1_url` TEXT,
  `entities_urls1_display_url` TEXT,
  `entities_urls1_expanded_url` TEXT,

  `entities_urls2_indices_start` INT,
  `entities_urls2_indices_end` INT,
  `entities_urls2_url` TEXT,
  `entities_urls2_display_url` TEXT,
  `entities_urls2_expanded_url` TEXT,

  `entities_urls3_indices_start` INT,
  `entities_urls3_indices_end` INT,
  `entities_urls3_url` TEXT,
  `entities_urls3_display_url` TEXT,
  `entities_urls3_expanded_url` TEXT,



  `entities_user_mentions0_name` TEXT,
  `entities_user_mentions0_indices_start` INT,
  `entities_user_mentions0_indices_end` INT,
  `entities_user_mentions0_screen_name` TEXT,
  `entities_user_mentions0_id_str` BIGINT,

  `entities_user_mentions1_name` TEXT,
  `entities_user_mentions1_indices_start` INT,
  `entities_user_mentions1_indices_end` INT,
  `entities_user_mentions1_screen_name` TEXT,
  `entities_user_mentions1_id_str` BIGINT,

  `entities_user_mentions2_name` TEXT,
  `entities_user_mentions2_indices_start` INT,
  `entities_user_mentions2_indices_end` INT,
  `entities_user_mentions2_screen_name` TEXT,
  `entities_user_mentions2_id_str` BIGINT,

  `entities_user_mentions3_name` TEXT,
  `entities_user_mentions3_indices_start` INT,
  `entities_user_mentions3_indices_end` INT,
  `entities_user_mentions3_screen_name` TEXT,
  `entities_user_mentions3_id_str` BIGINT,

  `entities_user_mentions4_name` TEXT,
  `entities_user_mentions4_indices_start` INT,
  `entities_user_mentions4_indices_end` INT,
  `entities_user_mentions4_screen_name` TEXT,
  `entities_user_mentions4_id_str` BIGINT,

  `entities_user_mentions5_name` TEXT,
  `entities_user_mentions5_indices_start` INT,
  `entities_user_mentions5_indices_end` INT,
  `entities_user_mentions5_screen_name` TEXT,
  `entities_user_mentions5_id_str` BIGINT,

  `entities_user_mentions6_name` TEXT,
  `entities_user_mentions6_indices_start` INT,
  `entities_user_mentions6_indices_end` INT,
  `entities_user_mentions6_screen_name` TEXT,
  `entities_user_mentions6_id_str` BIGINT,

  `entities_user_mentions7_name` TEXT,
  `entities_user_mentions7_indices_start` INT,
  `entities_user_mentions7_indices_end` INT,
  `entities_user_mentions7_screen_name` TEXT,
  `entities_user_mentions7_id_str` BIGINT,



  `entities_symbols_indices_start` INT,
  `entities_symbols_indices_end` INT,
  `entities_symbols_text` TEXT,

  `entities_polls_option1_text` TEXT,
  `entities_polls_option2_text` TEXT,
  `entities_polls_option3_text` TEXT,
  `entities_polls_option4_text` TEXT,
  `entities_polls_end_datetime` DATETIME,
  `entities_polls_duration_minutes` INT,


  `extended_entities_media0_media_url_https` TEXT,
  `extended_entities_media0_type` TEXT,
  `extended_entities_media1_media_url_https` TEXT,
  `extended_entities_media1_type` TEXT,
  `extended_entities_media2_media_url_https` TEXT,
  `extended_entities_media2_type` TEXT,
  `extended_entities_media3_media_url_https` TEXT,
  `extended_entities_media3_type` TEXT

);

CREATE TABLE favs (
  
  `added_at` DATETIME DEFAULT CURRENT_TIMESTAMP,

  `fav_by_screen_name` VARCHAR(256) NOT NULL,
  `id_str` BIGINT NOT NULL,

  `full_text` TEXT NOT NULL,
  `created_at` DATETIME,

  `source` TEXT,
  `in_reply_to_status_id_str` BIGINT,
  `in_reply_to_user_id_str` BIGINT,
  `in_reply_to_screen_name` TEXT,

  `is_quote_status` TINYINT,
  `quoted_status_id_str` BIGINT,
  `quoted_status` TEXT,

  `favorited` TINYINT,
  `retweeted` TINYINT,
  `retweet_count` INT,
  `favorite_count` INT,

  `possibly_sensitive` TINYINT,
  `filter_level` TEXT,

  `lang` TEXT,




  `user_id_str` BIGINT,
  `user_name` TEXT,
  `user_screen_name` TEXT,
  `user_location` TEXT,
  `user_url` TEXT,
  `user_description` TEXT,
  `user_protected` TINYINT,
  `user_verified` TINYINT,
  `user_followers_count` INT,
  `user_friends_count` INT,
  `user_listed_count` INT,
  `user_favourites_count` INT,
  `user_statuses_count` INT,
  `user_created_at` DATETIME,
  `user_profile_banner_url` TEXT,
  `user_profile_image_url_https` TEXT,
  `user_withheld_in_countries` TEXT,





  `place_place_type` TEXT,
  `place_name` TEXT,
  `place_full_name` TEXT,
  `place_country_code` TEXT,
  `place_country` TEXT,
  `place_bounding_box_coordinates_1Long` DOUBLE,
  `place_bounding_box_coordinates_1Lat` DOUBLE,
  `place_bounding_box_coordinates_2Long` DOUBLE,
  `place_bounding_box_coordinates_2Lat` DOUBLE,
  `place_bounding_box_coordinates_3Long` DOUBLE,
  `place_bounding_box_coordinates_3Lat` DOUBLE,
  `place_bounding_box_coordinates_4Long` DOUBLE,
  `place_bounding_box_coordinates_4Lat` DOUBLE,
  `place_bounding_box_type` TEXT,
  
  `coordinates_type` TEXT,
  `coordinates_coordinates_Long` DOUBLE,
  `coordinates_coordinates_Lat` DOUBLE,





  `entities_hashtags0_indices_start` INT,
  `entities_hashtags0_indices_end` INT,
  `entities_hashtags0_text` TEXT,

  `entities_hashtags1_indices_start` INT,
  `entities_hashtags1_indices_end` INT,
  `entities_hashtags1_text` TEXT,

  `entities_hashtags2_indices_start` INT,
  `entities_hashtags2_indices_end` INT,
  `entities_hashtags2_text` TEXT,

  `entities_hashtags3_indices_start` INT,
  `entities_hashtags3_indices_end` INT,
  `entities_hashtags3_text` TEXT,

  `entities_hashtags4_indices_start` INT,
  `entities_hashtags4_indices_end` INT,
  `entities_hashtags4_text` TEXT,

  `entities_hashtags5_indices_start` INT,
  `entities_hashtags5_indices_end` INT,
  `entities_hashtags5_text` TEXT,

  `entities_hashtags6_indices_start` INT,
  `entities_hashtags6_indices_end` INT,
  `entities_hashtags6_text` TEXT,

  `entities_hashtags7_indices_start` INT,
  `entities_hashtags7_indices_end` INT,
  `entities_hashtags7_text` TEXT,


  `entities_media0_display_url` TEXT,
  `entities_media0_expanded_url` TEXT,
  `entities_media0_id_str` BIGINT,
  `entities_media0_indices_start` INT,
  `entities_media0_indices_end` INT,
  `entities_media0_media_url` TEXT,
  `entities_media0_media_url_https` TEXT,
  `entities_media0_type` TEXT,
  `entities_media0_url` TEXT,

  `entities_media1_display_url` TEXT,
  `entities_media1_expanded_url` TEXT,
  `entities_media1_id_str` BIGINT,
  `entities_media1_indices_start` INT,
  `entities_media1_indices_end` INT,
  `entities_media1_media_url` TEXT,
  `entities_media1_media_url_https` TEXT,
  `entities_media1_type` TEXT,
  `entities_media1_url` TEXT,

  `entities_media2_display_url` TEXT,
  `entities_media2_expanded_url` TEXT,
  `entities_media2_id_str` BIGINT,
  `entities_media2_indices_start` INT,
  `entities_media2_indices_end` INT,
  `entities_media2_media_url` TEXT,
  `entities_media2_media_url_https` TEXT,
  `entities_media2_type` TEXT,
  `entities_media2_url` TEXT,

  `entities_media3_display_url` TEXT,
  `entities_media3_expanded_url` TEXT,
  `entities_media3_id_str` BIGINT,
  `entities_media3_indices_start` INT,
  `entities_media3_indices_end` INT,
  `entities_media3_media_url` TEXT,
  `entities_media3_media_url_https` TEXT,
  `entities_media3_type` TEXT,
  `entities_media3_url` TEXT,
  


  `entities_urls0_indices_start` INT,
  `entities_urls0_indices_end` INT,
  `entities_urls0_url` TEXT,
  `entities_urls0_display_url` TEXT,
  `entities_urls0_expanded_url` TEXT,

  `entities_urls1_indices_start` INT,
  `entities_urls1_indices_end` INT,
  `entities_urls1_url` TEXT,
  `entities_urls1_display_url` TEXT,
  `entities_urls1_expanded_url` TEXT,

  `entities_urls2_indices_start` INT,
  `entities_urls2_indices_end` INT,
  `entities_urls2_url` TEXT,
  `entities_urls2_display_url` TEXT,
  `entities_urls2_expanded_url` TEXT,

  `entities_urls3_indices_start` INT,
  `entities_urls3_indices_end` INT,
  `entities_urls3_url` TEXT,
  `entities_urls3_display_url` TEXT,
  `entities_urls3_expanded_url` TEXT,



  `entities_user_mentions0_name` TEXT,
  `entities_user_mentions0_indices_start` INT,
  `entities_user_mentions0_indices_end` INT,
  `entities_user_mentions0_screen_name` TEXT,
  `entities_user_mentions0_id_str` BIGINT,

  `entities_user_mentions1_name` TEXT,
  `entities_user_mentions1_indices_start` INT,
  `entities_user_mentions1_indices_end` INT,
  `entities_user_mentions1_screen_name` TEXT,
  `entities_user_mentions1_id_str` BIGINT,

  `entities_user_mentions2_name` TEXT,
  `entities_user_mentions2_indices_start` INT,
  `entities_user_mentions2_indices_end` INT,
  `entities_user_mentions2_screen_name` TEXT,
  `entities_user_mentions2_id_str` BIGINT,

  `entities_user_mentions3_name` TEXT,
  `entities_user_mentions3_indices_start` INT,
  `entities_user_mentions3_indices_end` INT,
  `entities_user_mentions3_screen_name` TEXT,
  `entities_user_mentions3_id_str` BIGINT,

  `entities_user_mentions4_name` TEXT,
  `entities_user_mentions4_indices_start` INT,
  `entities_user_mentions4_indices_end` INT,
  `entities_user_mentions4_screen_name` TEXT,
  `entities_user_mentions4_id_str` BIGINT,

  `entities_user_mentions5_name` TEXT,
  `entities_user_mentions5_indices_start` INT,
  `entities_user_mentions5_indices_end` INT,
  `entities_user_mentions5_screen_name` TEXT,
  `entities_user_mentions5_id_str` BIGINT,

  `entities_user_mentions6_name` TEXT,
  `entities_user_mentions6_indices_start` INT,
  `entities_user_mentions6_indices_end` INT,
  `entities_user_mentions6_screen_name` TEXT,
  `entities_user_mentions6_id_str` BIGINT,

  `entities_user_mentions7_name` TEXT,
  `entities_user_mentions7_indices_start` INT,
  `entities_user_mentions7_indices_end` INT,
  `entities_user_mentions7_screen_name` TEXT,
  `entities_user_mentions7_id_str` BIGINT,



  `entities_symbols_indices_start` INT,
  `entities_symbols_indices_end` INT,
  `entities_symbols_text` TEXT,

  `entities_polls_option1_text` TEXT,
  `entities_polls_option2_text` TEXT,
  `entities_polls_option3_text` TEXT,
  `entities_polls_option4_text` TEXT,
  `entities_polls_end_datetime` DATETIME,
  `entities_polls_duration_minutes` INT,
  
  `extended_entities_media0_media_url_https` TEXT,
  `extended_entities_media0_type` TEXT,
  `extended_entities_media1_media_url_https` TEXT,
  `extended_entities_media1_type` TEXT,
  `extended_entities_media2_media_url_https` TEXT,
  `extended_entities_media2_type` TEXT,
  `extended_entities_media3_media_url_https` TEXT,
  `extended_entities_media3_type` TEXT,

  PRIMARY KEY (fav_by_screen_name, id_str)
);



CREATE TABLE followings (

  `added_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `follower_id` BIGINT,
  `followee_id` BIGINT,
  `follower_screen_name` TEXT,
  `followee_screen_name` TEXT,
  `follower_name` TEXT,
  `followee_name` TEXT,
  PRIMARY KEY (follower_id, followee_id)
);



CREATE TABLE users (

  `added_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `user_id_str` BIGINT NOT NULL PRIMARY KEY,
  `user_name` TEXT,
  `user_screen_name` TEXT,
  `user_location` TEXT,
  `user_url` TEXT,
  `user_description` TEXT,
  `user_protected` TINYINT,
  `user_verified` TINYINT,
  `user_followers_count` INT,
  `user_friends_count` INT,
  `user_listed_count` INT,
  `user_favourites_count` INT,
  `user_statuses_count` INT,
  `user_created_at` DATETIME,
  `user_profile_banner_url` TEXT,
  `user_profile_image_url_https` TEXT,
  `user_withheld_in_countries` TEXT,
  
  `fav_count` INT DEFAULT 0,
  
  `last_tweet_fetch_time` DATETIME,
  `last_fav_fetch_time` DATETIME,
  `last_user_fetch_time` DATETIME,
  `last_followers_fetch_time` DATETIME,
  `last_friends_fetch_time` DATETIME

);



CREATE TABLE lists (

  `is_from_twitter` TINYINT NOT NULL,
  `key_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `added_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `subscribed_by` TEXT,

  `id_str` BIGINT,
  `name` TEXT,
  `uri` TEXT,
  `subscriber_count` INT,
  `member_count` INT,
  `mode` TEXT,
  `description` TEXT,
  `slug` TEXT,
  `full_name` TEXT,
  `created_at` DATETIME,
  `following` TINYINT,
  `user` LONGTEXT,
  `members` LONGTEXT,


  PRIMARY KEY (`key_id`)
);


















delimiter //
CREATE TRIGGER time_init
       BEFORE INSERT ON users
  FOR EACH ROW
  BEGIN

      IF new.last_tweet_fetch_time IS NULL THEN
          SET new.last_tweet_fetch_time = 19700101000000;
      END IF;
      IF new.last_fav_fetch_time IS NULL THEN
          SET new.last_fav_fetch_time = 19700101000000;
      END IF;
      IF new.last_user_fetch_time IS NULL THEN
          SET new.last_user_fetch_time = '1970-01-01 00:00:00';
      END IF;
      IF new.last_followers_fetch_time IS NULL THEN
          SET new.last_followers_fetch_time = '1970-01-01 00:00:00';
      END IF;
      IF new.last_friends_fetch_time IS NULL THEN
          SET new.last_friends_fetch_time = '1970-01-01 00:00:00';
      END IF;
  END;//
delimiter ;






----syntax memos

update AllFromTwitterAPI
set
	extracted = 0
where
	request_type = 'getAllNewFavsByScreenName'


SELECT
    COUNT(*)
FROM
    favs;

  