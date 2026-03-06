import re
import unicodedata

# 入力された文字列を正規化する:
def checker_text(text: str) -> str:

    # 文字列でない場合は空文字を返す
    if not isinstance(text, str):
        return ""

    # 全角英数字→半角、半角カナ→全角カタカナ
    normalized_text = unicodedata.normalize('NFKC', text)
    
    # 全角スペースを半角スペースに変換
    normalized_text = normalized_text.replace('　', ' ')

    # 先頭と末尾の空白を削除
    normalized_text = normalized_text.strip()

    # 複数のスペースを1つのスペースに統一
    normalized_text = re.sub(r'\s+', ' ', normalized_text)
    
    # 全ての英字を小文字に変換
    normalized_text = normalized_text.lower()
    
    # 特殊文字を除去
    r"""
        \w: 英数字とアンダースコア
        \s: 空白文字
        ぁ-ん: ひらがな
        ァ-ヶ: カタカナ
        一-龠: 漢字
    """
    cleaned_text = re.sub(r'[^\w\sぁ-んァ-ヶ一-龠]', '', normalized_text)

    return cleaned_text

def errnote_check(form):
    # setを使用することで重複をなくす
    unique_errors = set()

    # フィールドごとにエラーを取得
    for field_errors in form.errors.values():
        # エラーの値を取得
        for error in field_errors:
            unique_errors.add(error)
    
    return unique_errors