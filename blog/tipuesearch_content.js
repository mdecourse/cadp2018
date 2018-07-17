var tipuesearch = {"pages":[{"title":"About","text":"2018 機械設計工程系電腦輔助設計實習 課程倉儲: https://github.com/mdecourse/cadp2018 課程投影片: https://mdecourse.github.io/cadp2018/reveal 課程網誌: https://mdecourse.github.io/cadp2018/blog","tags":"misc","url":"https://mdecourse.github.io/cadp2018/blog/pages/about/"},{"title":"協同設計室(二)","text":"昨天, 採用 Fossil SCM 與 Stunnel 建置的 https://[2001:288:6004:17:0811::cd06] 虛擬主機網站已經初步完成. 大家從手機中的瀏覽器就可以直接連線 (因為已經都支援 IPv6 協定). 接下來必須將此 IPv6 網址與 cd06.kmol.info 對應之外, 還要取得此一網址的第三方簽署的數位簽章. IPv6 網址與符號名稱的設定, 必須在 DNS 伺服器中指定一組 AAAA 設定, 將兩者綁定, 而網址的數位簽章, 則採用 certbot 完成. Certbot 數位簽章 certbot 數位簽章的取得與設定, 是由 nginx 的一組 Python 延伸程式完成. 由於之前已經將 https 所使用的 443 埠號交給 Stunnel 使用, 但當時所採用的是 self-signed 的數位簽章, 並沒有登錄在公開的 public server 上. certbot 驗證網址的方式是透過 nginx 的連線完成, 因此接下來必須安裝 nginx , 使用的埠號為 http 協定的 port 80. 在 Ubuntu 18.04 中安裝 nginx , 執行: $ sudo apt install nginx 接著, 必須安裝 certbot 延伸程式: $ sudo apt-get update $ sudo apt-get install software-properties-common $ sudo add-apt-repository ppa:certbot/certbot $ sudo apt-get update $ sudo apt-get install python-certbot-nginx 其中, 在 Ubuntu 18.04 執行 sudo add-apt-repository ppa:certbot/certbot 並沒有完成, 但似乎不影響隨後的 python-cerbot-nginx 安裝. 這時為了保留原始 nginx 執行設定 /etc/nginx/sites-available/default, 必須以 sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default_orig 加以保留. 接著透過 $ sudo certbot --nginx 讓 certbot 自動設定所需的 https 連線參數, 即可取得 /etc/letsencrypt/live/cd06.kmol.info/fullchain.pem 與 /etc/letsencrypt/live/cd06.kmol.info/privkey.pem 等兩數位公鑰與私鑰檔案. 完成 certbot 指令後, /etc/nginx/sites-available/default 將會依使用者選擇要從 http 跳轉 https, 或不跳轉, 插入必要的設定修改, 取得數位簽章後, 以 sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default_cert 儲存 certbot 所修改的 nginx 設定. 接下來則將 /etc/nginx/sites-available/default 恢復為原先的 default_orig 版本, 因為這裡只讓 nginx 佔用 port 80, port 443 仍然必須交還給之前所設定的 Stunnel 服務. nginx 恢復原狀後, 可以利用 /etc/init.d/nginx restart 重新啟動. 而 /etc/stunnel/ 目錄中原有的 localhost.crt 與 localhost.key 改為 localhost_self.crt 與 localhost_self.key, 並從 /etc/letsencrypt/live/cd06.kmol.info/fullchain.pem 與 /etc/letsencrypt/live/cd06.kmol.info/privkey.pem 複製 public signed 的網址數位簽章, 分別複製為 /etc/stunnel/localhost.crt 與 localhost.key 後, 以 /etc/init.d/stunnel4 start 啟動. 假如一切正常, 使用者便可以連線到 https://cd06.kmol.info 與 http://cd06.kmol.info , 前者為 Fossil SCM 加上 Stunnel , 而後者則由 nginx 伺服.","tags":"Misc","url":"https://mdecourse.github.io/cadp2018/blog/Collaborative-Design-Laboratory-II.html"},{"title":"協同設計室","text":"2018 年春天, 在電腦輔助設計室旁的一間約十坪大小的空間, 成立了所謂的協同設計室, 希望透過多人協力一同, 解決與電腦及網路軟硬體相關問題. Windows 10 的更新之罪 Windows 10 自推出以來, 每一次的更新都掀起論戰, 連最近的 1803 升級, 也不 例外 . 許多網站更教導使用者如何阻止 Windows 10 更新, 因為微軟多多少少藉著更新, 強力放送自家相關產品與服務. 儘管這些置入性行銷不怎麼討喜, 但是從 Windows 7 到目前的 Windows 10, 微軟加諸在這一系列產品的用心, 令人印象深刻, 因此在這個階段, 協同設計室反而建議大家照單全收 Windows 10 的各項網路服務, 再過一段時間, 當大家都明確感受到 AI 人工智慧的貼心之後, 應該對於 Windows 10 緊密透過網路提供的各項置入性行銷, 就不會再有排拒之想了. 如何與還原卡共存 一旦決定與 Windows 10 的密集更新政策和好, 接下來電腦輔助設計室所面臨的問題是: 該如何與還原卡共存? 理論上, 作為每一學年有將近千人入學的機械工程群, 在新生報到時直接發給一台完整裝載合法套件, 並且至少保用四年的 17 吋筆電, 應該是最理想的規劃, 因為如此, 每一門課都可以沉浸在數位整合環境之中 (意思是學生除了上課滑手機之餘, 還可以滑筆電:-), 只是事與願違, 這個理想與貼在四週牆上的\"禁止使用非法軟體\"標語一樣, 超級與現實脫節 (這一定是玩笑話了). 在無法每位學員人手一台筆電的情況下, 幾乎每一時段都有兩門至四門的必修電腦課程時, 一個系所就必須維護大約 180 台 Windows 10, 總共四間 電腦教室, 而這些電腦都分別使用群準 EVOsys Pro v6 與 UEFI v8 還原卡, 因此接下來的議題是, 為數不少的 Windows 10 電腦該如何與還原卡共存? 除了勤作網路拷貝之外, 目前還找不到答案, 大家不要忘記: 我們已經決定舉雙手, 完全接受微軟 Windows 10 操作系統的各種密集更新! 電腦分類 目前電腦輔助設計室所使用的還原卡為 Evo Pro v6, 採 MBR (Master Boot Record) 分割硬碟, 而協同設計室則使用 Evo UEFI v8, 採用 GPT (GUID Partition Table) 格式分割硬碟. 其中, 電腦輔助設計室的電腦皆為 client, 而協同設計室則有 client 與 Virtualbox 上的 Ubuntu 18.04 LTS (Long Term Support) Server + ubuntu-desktop. 電腦輔助設計室共 65 台電腦的規格為: 華碩 Skylake MD790/I7-6700, Intel 第六代 Core i7/3.4GHz/8M CPU, 採用 Intel Q170 晶片組, 搭載 16GB DDR4/2133/288 Pin 記憶體 (8 GBx2), 2 TB-SATA3 硬碟, Asus MINI-GTX950-2G 顯示卡 (支援 PCIE 3.0, OpenGL 4.5, 768 個CUDA 核心數), 500瓦電源供應器, USB 3.1x2 (10GB/s) , USB 3.0x6 (5GB/s), USB 2.0x2 (480MB/s), 以及 群準的 EVOsys PRO v6 還原卡, 可同時支援 D-sub、HDMI 及 DisplayPort 三台獨立顯示器多工作業. 這批華碩電腦在安裝群準的 EVOsys PRO v6 還原卡之前, 必須先將 Asus UEFI BIOS Utility 中 Boot 功能表下的 secure boot 中的 OS Type, 由內建的 Windows UTFI OS 改為 Other OS, 否則無法在開機後導引到 EVOsys PRO v6 還原卡功能選項. 進入 EVOsys PRO v6 還原卡選項後, 以全新安裝分割硬碟, 一般 Windows 7 與 10 操作系統的資料類別為 A, Ubuntu 選 B, 而 swap 磁區則選擇 P, 分割完成後, 透過 EVOsys 所規劃的開機表單, 選擇 Windows 10 後按下 Enter, 可以進入該硬碟分隔磁區, 但是尚未安裝操作系統, 因此會出現無法開機提示, 這時以 Ctrl+Alt+Del 重新開機後, 可以透過 F8 導引到光碟機開機後進行 Windows 10 操作系統安裝, 這點與 EVOsys UEFI v8 版本功能有明顯差異, 因為 EVOsys UEFI v8 版本提供選擇開機表單中的操作系統選項後, 可以透過 Ctrl+i 執行操作系統安裝, 系統會直接導引到光碟機或 USB 開機選項. 至於協同設計室中的 CD06 電腦充作伺服器使用, 實體操作系統為 Windows 10, 內部則有兩台 Virtualbox 虛擬 Ubuntu 18.04 server + ubuntu-desktop, 虛擬主機與 Windows 10 同步啟動服務採用 vboxvmservice , /etc/netplan 中 IPv6 固定 IP YAML 檔案設定如下: network: ethernets: enp0s3: addresses: - 2001:288:6004:17:0811::cd06/64 gateway6: 2001:288:6004:17::254 nameservers: addresses: - 2001:b000:168::1 version: 2 虛擬 Ubuntu 18.04 中的 Fossil SCM Stunnel 與 Fossil SCM 安裝 sudo apt update sudo apt install stunnel4 -y sudo apt install fossil 環境變數與開機啟動設定 /etc/environment 設定: HTTPS=on /etc/default/stunnel4 檔案設定: ENABLED=1 Stunnel 設定並執行 fossil http 指令 首先在 /etc/stunnel 目錄中建立 localhost.key 與 localhost.crt: sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt /etc/stunnel/stunnel.conf 設定檔案, 可同時支援 IPv4 與 IPv6 協定: [https] accept = your_IPv4_ip:443 accept = :::443 cert = /etc/stunnel/localhost.crt key = /etc/stunnel/localhost.key exec = /usr/bin/fossil execargs = /usr/bin/fossil http /home/cdlab/repository/cdlab.fossil --https --nojail 其中 --nojail 目的在 drop the root privilege but do not enter the chroot jail 重新啟動 stunnel4 則使用 /etc/init.d/stunnel4 restart 建立 cdlab.fossil 則進入 /home/cdlab/repository 目錄後, 執行 fossil init cdlab.fossil 上述設定完成後, 重新開機即可以 https://[2001:288:6004:17:0811::cd06] 連結至 cdlab.fossil 網際管理介面.","tags":"Misc","url":"https://mdecourse.github.io/cadp2018/blog/Collaborative-Design-Laboratory.html"},{"title":"編譯 Fossil SCM","text":"在此利用 Msys2 編譯適用於 Windows 10 64 位元環境中的 Fossil SCM. 編譯流程 首先從 Gnuwin32 coreutils 取得視窗環境下執行的 cat 與 grep, 並且確定 sh.exe 位於指令搜尋路徑 (例如, 透過 git/bin 目錄中的 sh.exe), 先編譯 Fossil SCM 附帶的 zlib 後, 再設定 PREFIX = x86_64-w64-mingw32-, 就可順利完成 fossil.exe 的編譯. 在不修改 win/Makefile.mingw 的情況下, 必須與 zlib1.dll 配合才能執行. 若開啟 LIB = -static 設定, 則可以將程式庫納入 fossil.exe 中執行。 取得 fossil clone 原始碼 從 Fossil SCM 倉儲取得原始碼壓縮檔後, 在 wd/fossil 目錄中解開 trunk 最新版本的原始碼, 目前為 Fossil SCM 2.5 版. fossil clone https://www.fossil-scm.org fossil.fossil cd wd mkdir fossil cd fossil fossil open ./../../fossil.fossil 編譯 zlib 在 MSYS2 環境中編譯 Fossil SCM 時, 必須先編譯 compat/zlib cd compat/zlib mingw32-make -f win32/Makefile.gcc 編譯 fossil.exe 之後, 再退出 compat/zlib 目錄, 回到 wd/fossil 目錄中, 編輯 win/Makefile.mingw, 設定 PREFIX = x86_64-w64-mingw32- LIB = -static 接著以 mingw32-make -f win/Makefile.mingw 編譯 fossil.exe 根據以上說明所建立的教學用倉儲位於: https://github.com/kmolab/fossil-scm_25","tags":"Misc","url":"https://mdecourse.github.io/cadp2018/blog/msys2_compile_fossil_scm.html"}]};