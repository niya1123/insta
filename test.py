from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pprint

class QiitaGetRanking():
    """
    Qiitaからランキングデータを取得するクラス.
    """

    def get_tag_ranking(self, browser: webdriver) -> dict:
        """
        Qiitaからタグランキングに関する情報を取得する関数.

        Parameters
        ----------
        browser: webdrive
            スクレイピングするためのwebdriverのオブジェクト

        Returns
        -------
        tag_ranking_data: dict
            タグランキングを収めた辞書オブジェクト.
        """
        html = browser.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        ra_tag_names = soup.find_all(class_='ra-Tag_name pr-1')
        tag_ranking_data = {}
        for i, ra_tag_name in enumerate(ra_tag_names):
            tag_ranking_data[i+1] = [ra_tag_name.text, 
            'https://qiita.com/tags/%s'%(ra_tag_name.text.lower())]
        return tag_ranking_data

if __name__ == "__main__":
    """
    main文. browserはhtmlの取得が終わり次第閉じること.エラーが出てきたときも同様.
    """

    try:
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        print("start scrape")
        browser.get('https://qiita.com')
        # javascriptが全て読み込まれるまで待機. 15秒経っても読み込みが終わらなければタイムアウト判定.
        WebDriverWait(browser, 15).until(EC.presence_of_all_elements_located)
        print("generate object")
        qgr = QiitaGetRanking()
        ranking_data = qgr.get_tag_ranking(browser)
        browser.close()
        browser.quit()
        pprint.pprint(ranking_data)
    except:
        browser.close()
        browser.quit()