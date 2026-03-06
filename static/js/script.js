  // -------------------------
  // 変数を定義
  // -------------------------
  const menuBtn    = document.querySelector('.menu-button');        // ハンバーガーメニュー
  const menu       = document.querySelector('.slide-menu');         // スライドメニュー
  

  // メニューボタンクリック時にスライドメニューを開閉
  if (menuBtn && menu) {                            //ハンバーガーメニューとスライドメニューがあるか

    // メニューボタンクリック時の処理
    menuBtn.addEventListener('click', (ev) => {
      // イベントの発生を限定（閉じるクリックイベントに影響させないため）
      ev.stopPropagation(); 

      // メニューを開く      
      menu.classList.add('is-open');     
    });

    // メニュー外クリックで閉じる
    document.addEventListener('click', (ev) => {
      const isClickInsideMenu   = menu.contains(ev.target);      // クリック位置がメニュー内か判定
  
      // メニューが開いていて、かつメニュー外をクリックしたか
      if (menu.classList.contains('is-open') && !isClickInsideMenu ) {
        menu.classList.remove('is-open');                       // メニューを閉じる
      }
    });
  }






// -------------------------
// 変数を定義
// -------------------------
const searchBtn  = document.querySelector('.pc-menu-search');     // PC用検索ボタン
const search     = document.querySelector('.search-input-field'); // 検索入力フィールド
const headerLeft = document.querySelector('.header-left-group');  // ヘッダー左側のグループ


// 検索バーの開閉
if (searchBtn && search) {

  // 検索ボタンクリック時の処理
  searchBtn.addEventListener('click', (ev) => {
    // イベントの発生を限定（閉じるクリックイベントに影響させないため）
    ev.stopPropagation(); 

    // is-activeクラスがついていないか
    if (!search.classList.contains('is-active')) {
      search.classList.add('is-active');                  // is-activeクラスの追加

      // ヘッダー左側のグループがあるか
      if (headerLeft) {
        headerLeft.style.opacity = '0';                   // 透明にする
        headerLeft.style.pointerEvents = 'none';          // クリック不可にする
      }
      // 入力欄に自動フォーカス
      search.querySelector('.search-input').focus();
    }
  });

  // 検索バー外クリックで閉じる処理 
  document.addEventListener('click', (ev) => {
    const isClickInsideSearch = search.contains(ev.target);             // クリック位置が検索バー内か判定
    const isClickOnSearchBtn  = searchBtn.contains(ev.target);          // クリック位置が検索ボタンか判定
    const isSearchOpen        = search.classList.contains('is-active'); // 検索バーが開いているか判定

    // 検索バーが開いていて、かつ検索バー外・ボタン外をクリックしたか
    if (isSearchOpen && !isClickInsideSearch && !isClickOnSearchBtn) {
      // ヘッダー左側のグループがあるか
      if (headerLeft) {
        headerLeft.style.opacity = '1';                                 // 表示状態に戻す
        headerLeft.style.pointerEvents = 'auto';                        // クリック可能にする
      }
      search.classList.remove('is-active');                             // is-activeクラスを削除
    }
  });
};





// -------------------------
// 変数を定義
// -------------------------
const header = document.querySelector(".header");     // ヘッダー

// ウィンドウのスクロールイベントを監視
window.addEventListener("scroll", function () {
  // ヘッダーがあるか
  if (header) {
    // 現在のスクロール量がページ最上部から1px以上かどうかを判定  
    if (window.scrollY > 1) {
      // headerにis-scrolledクラスを追加（hover時と同じ変化）
      header.classList.add("is-scrolled");
    } else {
      // is-scrolledクラスを削除
      header.classList.remove("is-scrolled");
    }
  }
});






//　HTML要素に格納されたJSON文字列をJavaScriptオブジェクトに変換して返す
function getData(el, key) {
  return JSON.parse(el.dataset[key]);
}

// チャート幅に応じてフォントサイズを返す関数
function responsiveFont(context) {
  // 現在描画されているチャートの横幅を取得
  const w = context.chart.width;
  // フォントサイズを設定（400px:9px、400~700px:11px、700px:13px）
  const size = w < 400 ? 9 : w < 700 ? 11 : 13;
  return { size };
}




// 株価のみを表示するチャート

// -------------------------
// 変数を定義
// -------------------------
const priceEl = document.getElementById("priceChart"); // 株価チャート描画スペース

// 株価チャート描画スペースがあるか
if (priceEl) {

  // data属性からラベル（日付）と株価データを取得
  const labels = getData(priceEl, "labels");   // [日付:"2001-01-01", ...]
  const prices = getData(priceEl, "prices");   // [株価:100.5, 102.3, ...]

  priceEl.style.position = "absolute";
  priceEl.style.top = "0";
  priceEl.style.left = "0";
  priceEl.style.width = "100%";
  priceEl.style.height = "100%";

  // Chart.jsでグラフを生成
  const priceChart = new Chart(priceEl, {
    type: "line",                     // 折れ線グラフ

    // チャートデータの設定
    data: {
      labels: labels,                 // X軸のラベル（日付）
      datasets: [{
        label: "株価",                // データセットの名前
        data: prices,                 // Y軸のデータ（株価）
        borderColor: "#3b82f6",       // 線の色（青）
        borderWidth: 2,               // 線の太さ
        tension: 0.3,                 // 曲線の滑らかさ
        pointRadius: 0                // データポイントを非表示
      }]
    },

    // チャートオプションの設定
    options: {
      // レイアウト設定（余白）
      layout: {
        padding: {
          left: 48,                   // 左余白
          right: 48,                  // 右余白
          top: 24                     // 上余白
        }
      },
      responsive: true,              // レスポンシブ対応
      maintainAspectRatio: false,    // アスペクト比を固定しない

      // マウス操作時の動作設定
      interaction: {
        mode: "index",                // X軸の位置でデータを表示
        intersect: false              // 線上でなくてもツールチップ表示
      },

      // プラグイン設定
      plugins: {
        // 凡例の設定
        legend: {
          position: "bottom",         // 下部に配置
          labels: {
            usePointStyle: true       // ポイントスタイルを使用
          }
        },
        // ツールチップ（マウスホバー時の表示）設定
        tooltip: {
          callbacks: {
            // ラベル表示のカスタマイズ（小数点2桁まで表示）
            label: ctx =>
              `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(2)}`
          }
        }
      },

      // 軸の設定
      scales: {
        // X軸の設定
        x: {
          ticks: {
            autoSkip: false,                                  // 自動間引きを無効化
            maxRotation: 0,                                   // ラベルを回転させない
            minRotation: 0,                                   // ラベルを回転させない
            font: responsiveFont,                             // チャート幅に応じてフォントサイズを自動調整

            // ラベルを5年ごとに年号のみを表示し、同じ年の重複を防ぐ
            callback: function(value, index, values) {
              const label = this.getLabelForValue(value);     // ラベル文字列を取得
              const year = parseInt(label.slice(0, 4), 10);   // 年を抽出（最初の4文字）

              // チャート幅に応じて間隔を変える
              const w = this.chart.width;
              const interval = w < 400 ? 20 : w < 700 ? 10 : 5;  // 400px未満:20年、~700px:10年、700px以上:5年

              // 間隔の倍数でなければ表示しない
              if (year % interval !== 0) {
                return "";
              }

              // 同じ年が連続する場合は表示しない
              if (index > 0) {
                const prevLabel = this.getLabelForValue(values[index - 1].value);
                const prevYear = parseInt(prevLabel.slice(0, 4), 10);
                if (year === prevYear) {
                  return "";
                }
              }

              // 条件をクリアした場合のみ年を表示
              return year;
            }
          },

          //  縦のグリッド線（罫線）を5年ごとに表示
          grid: {
            display: true,                        // グリッド線を表示
            drawOnChartArea: true,                // チャートエリアに描画
            // ラベルが空文字の場合はグリッド線も引かないようにする
            color: (context) => {
              if (context.tick && context.tick.label === "") {
                return "transparent";             // 透明（非表示）
              }
              return "rgba(0, 0, 0, 0.1)";      // グレー
            }
          }
        },

        // Y軸の設定（株価）
        y: {
          position: "left",                       // 左側に配置
          title: { display: false },              // 軸タイトルは非表示
          ticks: {
            callback: v => v.toFixed(0),          // 値を整数で表示
            font: responsiveFont                  // チャート幅に応じてフォントサイズを自動調整
          }
        }
      }
    }
  });
}




// 積立シミュレーションを表示するチャート

// -------------------------
// 変数を定義
// -------------------------
const simEl = document.getElementById("simChart");      // シュミレーションチャート描画スペース



// シュミレーションチャート描画スペースがあるか
if (simEl) {

  // カスタムプラグインの定義
  const yAxisLabelPlugin = {
    id: "yAxisLabelPlugin",

    // 描画完了後に実行
    afterDraw(chart) {
      // X軸ラベルのレスポンシブ対応
      const w = chart.width;                            // 現在描画されているチャートの横幅を取得
      const limit = w < 400 ? 4 : w < 700 ? 6 : 8;      // ラベル数の上限（400px:4ヶ、400~700px:6ヶ、700px:8ヶ）
      chart.options.scales.x.ticks.maxTicksLimit = limit; 

      // Y軸ラベルの設定
      const { ctx, chartArea } = chart;                 // Canvasコンテキストとチャートエリアを取得
      ctx.save();                                       // 現在の描画状態を保存
      ctx.fillStyle = "#374151";                      // テキストの色（グレー）
      ctx.font = "12px sans-serif";                     // フォント設定
      ctx.textBaseline = "top";                         // テキストの基準位置

      // 左Y軸（株価）のラベルを描画
      ctx.textAlign = "left";                           // 左揃え
      ctx.fillText(
        "株価",
        chartArea.left - 40,                            // X座標（チャートの左端から-40px）
        chartArea.top - 20                              // Y座標（チャートの上端から-20px）
      );

      // 右Y軸（金額）のラベルを描画
      ctx.textAlign = "right";                          // 右揃え
      ctx.fillText(
        "金額（円）",
        chartArea.right + 40,                           // X座標（チャートの右端から+40px）
        chartArea.top - 20                              // Y座標（チャートの上端から-20px）
      );

      ctx.restore();                                    // 描画状態を元に戻す
    }
  };

  // Chart.jsでグラフを生成
  new Chart(simEl, {
    type: "line",                                       // 折れ線グラフ

    // チャートデータの設定 
    data: {
      labels: getData(simEl, "labels"),                 // X軸のラベル（日付）
      datasets: [
        // 折れ線1：株価（左Y軸）
        {
          label: "株価",
          data: getData(simEl, "prices"),               // 株価データ
          yAxisID: "y",                                 // 左Y軸を使用
          borderColor: "#3b82f6",                     // 線の色（青）
          borderWidth: 2,                               // 線の太さ
          tension: 0.3,                                 // 曲線の滑らかさ
          pointRadius: 0                                // データポイントを非表示
        },

        // 折れ線2：積立額（右Y軸）
        {
          label: "積立額",
          data: getData(simEl, "invested"),             // 積立額データ
          yAxisID: "y1",                                // 右Y軸を使用
          borderColor: "#ef4444",                     // 線の色（赤）
          borderWidth: 2,                               // 線の太さ
          borderDash: [6, 6],                           // 破線スタイル（6pxの線、6pxの空白）
          tension: 0,                                   // 直線（曲線なし）
          pointRadius: 0                                // データポイントを非表示
        },

        // 折れ線③：評価額（右Y軸・塗りつぶしあり）
        {
          label: "評価額",
          data: getData(simEl, "valuation"),            // 評価額データ
          yAxisID: "y1",                                // 右Y軸を使用
          borderColor: "#f59e0b",                     // 線の色（オレンジ）
          backgroundColor: "rgba(245,158,11,0.25)",   // 塗りつぶしの色（半透明オレンジ）
          fill: true,                                   // エリアを塗りつぶす
          borderWidth: 3,                               // 線の太さ
          tension: 0.25,                                // 曲線の滑らかさ
          pointRadius: 0                                // データポイントを非表示
        }
      ]
    },

    // チャート全体のオプション設定
    options: {
      // レイアウト設定（余白）
      layout: {
        padding: {
          left: 48,
          right: 48,
          top: 24
        }
      },
      responsive: true,                                 // レスポンシブ対応
      maintainAspectRatio: false,                       // CSSで指定した高さを優先

      // マウス操作時の動作設定
      interaction: {
        mode: "index",                                  // X軸の位置でデータを表示
        intersect: false                                // 線上でなくてもツールチップ表示
      },

      // プラグイン設定
      plugins: {
        // 凡例の設定
        legend: {
          position: "bottom",                           // 下部に配置
          labels: {
            usePointStyle: true                         // ポイントスタイルを使用
          }
        },

        // ツールチップ設定
        tooltip: {
          callbacks: {
            // ラベル表示のカスタマイズ
            label: ctx => {
              const v = ctx.parsed.y;
              // 右Y軸（金額）はカンマ区切り＋円マーク
              if (ctx.dataset.yAxisID === "y1") {
                return `${ctx.dataset.label}: ${v.toLocaleString()}円`;
              }
              // 左Y軸（株価）は小数点表示
              return `${ctx.dataset.label}: ${v.toFixed(2)}`;
            }
          }
        }
      },

      // 軸の設定
      scales: {
        // X軸の設定
        x: {
          ticks: {
            autoSkip: true,           // 自動間引きを有効化
            maxTicksLimit: 8,         // 最大8個までラベルを表示
            maxRotation: 0,           // ラベルを回転させない
            minRotation: 0,           // ラベルを回転させない
            font: responsiveFont      // チャート幅に応じてフォントサイズを自動調整
          }
        },

        // 左Y軸の設定（株価）
        y: {
          position: "left",           // 左側に配置
          title: { display: false },  // プラグインで描画
          ticks: {
            callback: v => v.toFixed(0),  // 値を整数で表示
            font: responsiveFont          // チャート幅に応じてフォントサイズを自動調整
          }
        },

        // 右Y軸の設定（金額）
        y1: {
          position: "right",                // 右側に配置
          grid: { drawOnChartArea: false }, // グリッド線を描画しない（重複防止）
          title: { display: false },        // プラグインで描画
          ticks: {
            callback: v => v.toLocaleString(),  // 値をカンマ区切りで表示
            font: responsiveFont                // チャート幅に応じてフォントサイズを自動調整
          }
        }
      }
    },
    plugins: [yAxisLabelPlugin]             // カスタムプラグインを登録
  });
}

