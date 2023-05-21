from facebook_ads_downloader import save_data, scrape_facebook
import sys

if __name__ == '__main__':
    print(sys.argv)
    df = scrape_facebook("https://www.facebook.com/", "../cookies.txt", posts_limit=5)
    print(df)
    save_data(df, "")