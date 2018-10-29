library(tidyverse)
# library(data.table)


id_attention <- c(25, 246)

(df_sample <-
  read_csv("~/projects/Mindfirl _old/MINDFIRL-userstudy/ppirl-userstudy/data/samples_sections_scrambling/section_1_sample_1.csv",
    col_names = F,
    col_types = cols(.default = "c")
  ) %>%
  select(1:9) %>%
  filter(row_number() <= 2 * 6 * 2) %>%
  select(-X3, -X6) %>%
  filter(!X1 %in% id_attention) %>%
  mutate_all(function(x) {
    x[is.na(x)] <- ""
    x
  }))
colnames(df_sample) <- c("ID", "voter_reg_num", "first_name", "last_name", "dob", "sex", "race")

df_sample_p1 <-
  df_sample %>% 
  group_by(ID) %>%
  slice(1) %>%
  ungroup() %>%
  mutate(ID = ID %>% str_c("_a")) 

df_sample_p2 <-
  df_sample %>%
  group_by(ID) %>%
  slice(2) %>%
  ungroup() %>%
  mutate(ID = ID %>% str_c("_a")) 

df_pair <-
  bind_rows(
    df_sample_p1,
    df_sample_p2
  ) %>%
  arrange(ID)

df_sample_p1 %>%
  write_csv("~/projects/mindfirl/mindfirl/data/tests/test_1_sample_1.csv")
df_sample_p2 %>%
  write_csv("~/projects/mindfirl/mindfirl/data/tests/test_1_sample_2.csv")
df_pair %>%
  write_csv("~/projects/mindfirl/mindfirl/data/tests/test_1_pair.csv")


(df_sample <-
  read_csv("~/projects/Mindfirl _old/MINDFIRL-userstudy/ppirl-userstudy/data/samples_sections_scrambling/section_1_sample_1.csv",
    col_names = F,
    col_types = cols(.default = "c")
  ) %>%
  select(1:9) %>%
  filter(row_number() %>% between(2 * 6 * 2 + 1, 2 * 6 * 3)) %>%
  select(-X3, -X6) %>%
  filter(!X1 %in% id_attention) %>%
  mutate_all(function(x) {
    x[is.na(x)] <- ""
    x
  }))

colnames(df_sample) <- c("ID", "voter_reg_num", "first_name", "last_name", "dob", "sex", "race")

df_sample_p1 <-
  df_sample %>%
  group_by(ID) %>%
  slice(1) %>%
  ungroup() %>%
  mutate(ID = ID %>% str_c("_a")) 

df_sample_p2 <-
  df_sample %>%
  group_by(ID) %>%
  slice(2) %>%
  ungroup() %>%
  mutate(ID = ID %>% str_c("_b")) 


bind_rows(
  df_sample_p1,
  df_sample_p2
) %>%
  arrange(ID) %>%
  print(n = Inf)

df_sample_p2_tmp <-
  df_sample_p2 %>%
  filter(last_name %>% str_detect("SHORE") |
    first_name %>% str_detect("BAKRI") |
    dob %>% str_detect("04/08/1928"))

df_sample_p2_tmp[df_sample_p2_tmp$first_name == "BAKRI", "first_name"] <- "BAKER"
df_sample_p2_tmp[df_sample_p2_tmp$first_name == "BAKER", "dob"] <- "04/08/1982"
df_sample_p2_tmp[df_sample_p2_tmp$first_name == "ERNEST", "last_name"] <- "SHORE"
df_sample_p2_tmp$ID <- df_sample_p2_tmp$ID %>% str_c("d")

df_sample_p2 <-
  bind_rows(
    df_sample_p2,
    df_sample_p2_tmp
  )

df_pair <-
  bind_rows(
    df_sample_p1,
    df_sample_p2
  ) %>%
  arrange(ID)

df_sample_p1 %>%
  write_csv("~/projects/mindfirl/mindfirl/data/tests/test_2_sample_1.csv")
df_sample_p2 %>%
  write_csv("~/projects/mindfirl/mindfirl/data/tests/test_2_sample_2.csv")
df_pair %>%
  write_csv("~/projects/mindfirl/mindfirl/data/tests/test_2_pair.csv")
%>% 
