import streamlit as st
import json
import os
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Configure page
st.set_page_config(
    page_title="A Letter Just for You",
    page_icon="💌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling - FIXED VERSION
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower:wght@400&family=Dancing+Script:wght@400;500;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

/* Reset and base styles */
* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
    overflow-x: hidden;
}

body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

/* Main container with proper spacing */
.main-container {
    background: linear-gradient(135deg, #fdf6e3 0%, #f4f1e8 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1rem;
    position: relative;
}

/* Streamlit app container fixes */
.stApp {
    margin: 0;
    padding: 0;
}

.stApp > div {
    padding-top: 0;
}

/* Login container */
.login-container {
    background: rgba(255, 255, 255, 0.9);
    padding: 3rem 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 2px solid #e8dcc0;
    text-align: center;
    max-width: 400px;
    margin: 2rem auto;
    backdrop-filter: blur(10px);
    width: 100%;
}

/* Letter container */
.letter-container {
    background: #fdf6e3;
    background-image: 
        linear-gradient(90deg, #f0e6d2 1px, transparent 1px),
        linear-gradient(#f0e6d2 1px, transparent 1px);
    background-size: 20px 20px;
    padding: 3rem 2.5rem;
    margin: 2rem auto;
    max-width: 700px;
    width: 100%;
    border-radius: 15px;
    box-shadow: 
        0 0 0 1px #d4c5a0,
        0 5px 15px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.5);
    position: relative;
    transform: perspective(1000px) rotateX(2deg);
}

.letter-container::before {
    content: '';
    position: absolute;
    top: -5px;
    left: -5px;
    right: -5px;
    bottom: -5px;
    background: linear-gradient(45deg, #d4c5a0, #e8dcc0, #d4c5a0);
    border-radius: 20px;
    z-index: -1;
}

.letter-header {
    font-family: 'Dancing Script', cursive;
    font-size: 2.5rem;
    color: #8b4513;
    text-align: center;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.letter-content {
    font-family: 'Indie Flower', cursive;
    font-size: 1.3rem;
    line-height: 1.8;
    color: #5d4e37;
    text-align: left;
    margin-bottom: 2rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

.letter-signature {
    font-family: 'Dancing Script', cursive;
    font-size: 1.8rem;
    color: #8b4513;
    text-align: right;
    margin-top: 2rem;
    font-style: italic;
}

.envelope-icon {
    font-size: 4rem;
}

.login-title {
    font-family: 'Dancing Script', cursive;
    font-size: 2.2rem;
    color: #8b4513;
    margin-bottom: 1.5rem;
}

.error-message {
    color: #d4851c;
    font-family: 'Indie Flower', cursive;
    font-size: 1.1rem;
    padding: 1rem;
    background: rgba(212, 133, 28, 0.1);
    border-radius: 10px;
    border-left: 4px solid #d4851c;
    margin-top: 1rem;
}

.success-message {
    color: #2d5a27;
    font-family: 'Indie Flower', cursive;
    font-size: 1.1rem;
    text-align: center;
    margin-top: 1rem;
}

.download-section {
    text-align: center;
    margin: 3rem auto 2rem auto;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 15px;
    border: 2px dashed #d4c5a0;
    max-width: 600px;
    width: 100%;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-container {
        padding: 1rem 0.5rem;
    }
    
    .login-container {
        padding: 2rem 1.5rem;
        margin: 1rem auto;
    }
    
    .letter-container {
        padding: 2rem 1.5rem;
        margin: 1rem auto;
        transform: none;
    }
    
    .letter-header {
        font-size: 2rem;
    }
    
    .letter-content {
        font-size: 1.1rem;
    }
    
    .letter-signature {
        font-size: 1.5rem;
    }
}

/* Safe footer hiding - prevents crashes */
footer[data-testid="stDecoration"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}

div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
}

/* Header hiding */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Main menu hiding */
#MainMenu {
    visibility: hidden;
    height: 0%;
}

/* Streamlit footer text hiding */
footer {
    visibility: hidden;
    height: 0%;
}

footer:after {
    content: '';
    visibility: visible;
    display: block;
    position: relative;
    padding: 5px;
    top: 2px;
}

/* Ensure content doesn't get cut off */
.main .block-container {
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Fix any overflow issues */
.stApp > div > div > div > div {
    overflow-x: hidden;
}
</style>
""", unsafe_allow_html=True)

# Sample data structure (in production, this would be in a secure database)
USERS_DATA = {
    "alma": {
        "password": "BESTIE",
        "letter": """My Dearest alma,

Heyyyooo Besssss ~~~🤠🤠
UHUYYYY AVVA NIICCHHHH 🤨
AVVAAN YAKK🤔
AVVA SIHHHH😶
GATAU AKUUUUUU🤥🤥

heheheheehe....😗😗😗😗
HEPIBESDEY TU YU🤗🥳🥳🤩🙉🐣💐💐
EPERIBADI LOP YU🥰🥰😘
CIHUYYYYY💃🏻💃🏻💃🏻💃🏻💃🏻
WAKTU YANG DINANTI TELAH TIBAAAA🕺🏻🕺🏻🕺🏻
BESTIKU SUDA BECALLLLL🔞🔞🔞🔞
UMUR BRPA SIH KAU, AKU LAGI PARNO KLO BAHAS UMUR SOALNYA :))
EALAHHH BARU 19+ BLM 21+ IEU MAHHHH😏
MET HARI BROJOL YA BEBBBBB😚😋😋
HUHUHUHU AKU SAYANG KAMUUUU MA BESTIIII MMMUUAACHHH😚😚😚😚💗💗💗💗💗💗💗

HARAPANKUUUU~
SEMOGAAAA🤲🏻🤲🏻
ALMAWADDATUL HUSNAAAAAA🥰🥰🥰
DI UMUR KE-19 INIIII 1️⃣9️⃣
BISA LEPAS DARI SEGALA KE OVT-AN NYAAAA😇😇😇
BISA LEBIH DEWASAAAAA (BKN KEARAH SONO YAH)👀👁🫦👁
DEWASA DALAM MENGAMBIL KEPUTUSAN🫂🫂🫂
GAK GAMPANG DOWN LAGIIII🫵🏻🫂❤‍🩹❤‍🩹❤‍🩹
HARUS SEMANGAT KULIAH NYA BEBB❣❣❣❣❣❣
SEMANGAT BERTAHAN HIDUUPPP💞😌💪🏻
HIDUPLAH LEBIH LAMA YA BESTIIII💋💋💋💋
BUKTIKAN KE SEMUA KLO ALMA ITU BEUHHH DABESSTTTT🫰🏻🫰🏻🫰🏻🤟🏻
HOPE U'RE ALWAYS HAPPY
SENDING U POSITIF VIBES FOR A HEALTHY AND HAPPY LIFE🫶🏻🫶🏻😽😽😽
SEMOGA JUGAAA SEGERA DIPERMUDAH PERCINTAAN MU YA BESSS🥴😚😚
NDANG NIKAH AJA🤪 GAPAPAA🙂‍↕
AKU MAU GENDONG PONAKAN😍😍
CHECK IN SOKINN DAHHH🤓🤓🤓
HEHEHEHE😁😁😁

MAKASIH YA BESSS SELALU ADA BUAT AI🥹🥹🥹🥹
DARI UMUR MU YG 19 INI
ENGKAU SUDAH DEDIKASIKAN 3 TAHUN BUAT MENGABDI KEPADAKU BWHAHAHAHA😀😀😀😀😀😀
SEBAGAIMANA KAMU SELALU ADA BUAT AKU
AKU JUGA AKAN NGELAKUIN HAL YANG SAMAAA😼😼😼
AKU BAKAL BERUSAHA SELALU ADA BUAT KAMUUU🫂🫂🫂🫶🏻🫶🏻🫶🏻
MAAF YA BESSS KLO BESTIMU INI TIDAK SEMPURNA😕😕
MASIH BYK KURANGNYAA HIKS WAJARLAH MANUSIA BUKAN NABI BOYY🤓🤙🏻 EKEKEKEKK🤣🤣🤣

BARENG-BARENG TERUS YAAAAA🙆🏻‍♀🙆🏻‍♀🙆🏻‍♀
AYO SUKSES BARENG, NIKAH BARENG, PUNYA ANAK BARENG, MENUA BARENG, SESURGA BARENG✨✨✨✨
HIKSSSS BESTIKU🤧🤧🤧 TERLUP-LUP INI TIDAK TERGANTIKAN POKOKNA MAH🥴🫰🏻
SEMANGAT TERUSSS POKOKNYAA, AKU SELALU DUKUNG KAMU BEBBB🙋🏻‍♀🙋🏻‍♀🙋🏻‍♀
MESKIPUN KITA JARANG KETEMU, AKU SELALU BERDOA BUAT KAMU BESS🫂
SEMOGA PERTEMANAN INI MAKIN KUAT🫱🏻‍🫲🏻🫱🏻‍🫲🏻
DAN NGAJARIN KITA UNTUK LEBIH MENGERTI SATU SAMA LAIN🫴🏻

MUNGKIN KELIATANNYA UCAPAN KU 11 12 KYK TAHUN SEBELUMNYA😢
TAPI AKU HARAP MESKIPUN DOA KU SELALU SAMA TAPI KMU HARUS TERUS BERKEMBANG YA BESS😉😉😉
JADI MANUSIA SEBAIK2 MANUSIA, CIAILAH😙
SAYANGI KEDUA ORTUMU, LALU SUAMIMU, LALU BESTIMU INI HIHIHI😘🥰😍
GREAT HOPE U CAN GET OVERALL THE STRUGGLES THAT COME INTO UR LIFE🥶🥶
KLO KMU BUTUH DIDENGERIN U KNOW WHO TO CALL😽😽

BTW KAU GABOLE NGECE AKU MAU 20😒
HABIS INI KAU JUGA 20😏
KUALAT LHO NANTI🙂‍↔
WLEEKKKK😝

DI ULTAH KE-19 INI MUNGKIN AKU BARU BISA KASIH UCAPAN INI SAMA KARYA FOTO KITA👉🏻👈🏻
AKU BELUM BISA KASIH KADO LANGSUNG KYK TAHUN SEBELUMNYA😔
TAPI TENANG BESSS😉
KADO AKAN MENYUSUL MU KE MALANG~~~ MWHEHEHEHE😋😋😋
DOAKAN AJA YAH (jujurly aku gk megang uang samsek soalnya)🤧
(rill lho bes bukannya aku gk mau ngado atau nyepelein atau gmn,
suwer ieu mah dah sebulan full aku mikir gmn cara ngadoin kamu,
tapi rejeki tak kunjung datang, hiksss, sabar ya bess, sekali lagi maaf blm bisa kasih kado langsung)
HOPE U LIKE IT DEH, NIH FOTO DIBUAT KHUSUS UNTUKMU~~🥴🫰🏻✨

MAYBE ENOUGH FROM ME🙂‍↕
MASIH BANYAK HAL YANG GAK AKAN MUAT KLO KU TULIS DISINI☝🏻
SAATNYA KAMU BERDOA AKU YG AAMIIN IN🤲🏻
LONG LASTING YA BES
EH I MEAN LONG LIFE~~
SEKALI LAGI SELAMAT BERTAMBAH UMURRRR🥳🥳🥳1️⃣9️⃣ (BERKURANG DING)
ENJOY CUZ THIS UR DAYYYYY💁🏻‍♀💁🏻‍♀🐣🐣""",
        "signature": "Your loving friend Syakira"
    },
    
    "Syakira": {
        "password": "SAYANG",
        "letter": """Dear Sayangku,

"Terima kasih, ya..."

Terima kasih, ya...
Untuk semua waktu yang kamu sisihkan — entah hanya untuk membalas pesan yang kelihatan sepele, atau untuk sekadar bilang, "jangan lupa minum air putih, ya sayang."

Aku tahu, mungkin dari luar terlihat biasa saja. Tapi ketika tubuhku lemas, kepala berat, dan pikiran berkabut karena sakit yang nggak juga reda, perhatian sekecil itu rasanya seperti cahaya kecil di ujung lorong gelap.

Dalam kondisi aku yang tidak sedang dalam versi terbaikku — murung, mudah tersinggung, sering diam, dan bahkan tak jarang mengeluh — kamu tetap di sana. Kamu tetap jadi kamu yang lembut, sabar, dan hadir. Tanpa banyak menuntut, tanpa mengeluh, bahkan kadang kamu yang lebih khawatir daripada aku sendiri.

Aku mungkin tidak terlalu pandai menunjukkan rasa terima kasih ini. Tapi sungguh, dalam diamku yang tak selalu bisa bicara jujur tentang sakit ini, hatiku terus berkata: "Untung ada kamu."

Kamu tahu, ada sesuatu yang hangat saat tahu aku tidak sendiri.
Sesuatu yang menenangkan, ketika melihat seseorang tetap memilih bertahan, meski yang dilihatnya bukanlah senyum cerah atau tawa bahagia, tapi keringat dingin, kantung mata, dan napas yang berat karena tubuh sedang kalah melawan rasa sakit.

Kehadiranmu itu bukan hanya menemani — tapi meneguhkan. Bahwa dicintai bukan soal kapan aku kuat dan lucu, tapi juga saat aku rapuh, lemah, dan penuh keluhan. Bahwa kamu bukan hanya datang untuk berbagi tawa, tapi juga bersedia duduk diam menemani tangis yang tak terdengar.

Dan aku belajar sesuatu minggu ini: bahwa kesetiaan bukan hanya tentang waktu yang panjang, tapi tentang niat untuk tetap tinggal, ketika satu-satunya hal yang bisa kuberikan adalah kata-kata pelan dan raut lelah.

Terima kasih, sayang.
Untuk tetap di sini, bahkan ketika tidak ada pelukan yang bisa kuberikan.
Untuk tidak pergi, bahkan saat yang bisa kamu genggam cuma tangan dingin yang lemas.
Untuk bersabar, meski aku bukan pasangan yang menyenangkan selama aku sakit.

Kalau aku bisa sembuh lebih cepat, mungkin salah satu alasannya adalah karena kamu membuat hari-hariku lebih ringan. Karena kamu membuat rasa sakit ini terasa tidak terlalu menakutkan.

Dan ketika nanti aku sudah benar-benar sembuh, izinkan aku membalas semua ketulusanmu.
Tidak hanya dengan tindakan, tapi juga dengan cinta yang tumbuh lebih dalam dari sebelumnya. Karena aku tahu, orang yang tetap tinggal di musim hujan, layak disambut hangat di musim semi.

Sekali lagi...
Terima kasih, ya. 🕊️,""",
        "signature": "Someone who values you greatly 🌟"
    }
}

def create_letter_image(name, letter_content, signature):
    """Create a PNG image of the letter"""
    try:
        # Create a large canvas
        width, height = 800, 1200  # Made taller to accommodate more content
        img = Image.new('RGB', (width, height), color='#fdf6e3')
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fallback to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 32)
            content_font = ImageFont.truetype("arial.ttf", 16)
            signature_font = ImageFont.truetype("arial.ttf", 20)
        except:
            # Fallback to default font with size
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            signature_font = ImageFont.load_default()
        
        # Draw decorative border
        border_color = '#d4c5a0'
        draw.rectangle([20, 20, width-20, height-20], outline=border_color, width=3)
        draw.rectangle([30, 30, width-30, height-30], outline=border_color, width=1)
        
        # Draw title
        title = f"A Letter for {name} ✨"
        try:
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
        except:
            # Fallback for older PIL versions
            title_width = len(title) * 20
        
        title_x = (width - title_width) // 2
        draw.text((title_x, 60), title, fill='#8b4513', font=title_font)
        
        # Draw letter content
        y_position = 120
        margin = 60
        line_height = 25
        max_y = height - 100  # Leave space for signature
        
        # Split content into lines that fit the width
        words = letter_content.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            try:
                bbox = draw.textbbox((0, 0), test_line, font=content_font)
                text_width = bbox[2] - bbox[0]
            except:
                # Fallback calculation
                text_width = len(test_line) * 10
            
            if text_width <= width - 2 * margin:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line with overflow protection
        for line in lines:
            if y_position >= max_y:
                lines_remaining = len(lines) - lines.index(line)
                if lines_remaining > 1:
                    draw.text((margin, y_position), "... (content continues)", 
                             fill='#8b4513', font=content_font)
                break
            
            draw.text((margin, y_position), line, fill='#5d4e37', font=content_font)
            y_position += line_height
        
        # Draw signature
        signature_y = max(y_position + 40, height - 80)
        draw.text((width - 300, signature_y), signature, fill='#8b4513', font=signature_font)
        
        return img
        
    except Exception as e:
        st.error(f"Error creating image: {str(e)}")
        # Return a simple fallback image
        img = Image.new('RGB', (400, 300), color='#fdf6e3')
        draw = ImageDraw.Draw(img)
        draw.text((50, 150), f"Letter for {name}", fill='#8b4513')
        return img

def get_image_download_link(img, filename):
    """Generate a download link for the image"""
    try:
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        b64 = base64.b64encode(buffer.read()).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="{filename}" style="text-decoration: none;">'
        return href
    except Exception as e:
        st.error(f"Error generating download link: {str(e)}")
        return ""

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Add error handling wrapper
try:
    # Main app logic
    if not st.session_state.authenticated:
        # Login page
        st.markdown("""
        <div class="main-container">
            <div class="login-container">
                <div class="envelope-icon">💌</div>
                <div class="login-title">A Letter Just for You</div>
                <p style="font-family: 'Indie Flower', cursive; color: #8b4513; font-size: 1.1rem; margin-bottom: 2rem;">
                    Someone special has written you a personal letter. Enter your details to open it.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            name = st.text_input("Your Name", placeholder="Enter your name...")
            password = st.text_input("Password", type="password", placeholder="Enter your password...")
            submitted = st.form_submit_button("Open My Letter ✨", use_container_width=True)
            
            if submitted:
                name_lower = name.lower().strip()
                if name_lower in USERS_DATA and USERS_DATA[name_lower]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.current_user = name_lower
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="error-message">
                        Oops, that didn't work. Please check your name and password and try again. 💫
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Letter display page
        user_data = USERS_DATA[st.session_state.current_user]
        user_name = st.session_state.current_user.title()
        
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Letter container
        st.markdown(f"""
        <div class="letter-container">
            <div class="letter-header">Hello, {user_name} ✨</div>
            <div class="letter-content">
                {user_data['letter'].replace(chr(10), '<br><br>')}
            </div>
            <div class="letter-signature">{user_data['signature']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download section
        st.markdown("""
        <div class="download-section">
            <h3 style="font-family: 'Dancing Script', cursive; color: #8b4513; margin-bottom: 1rem;">
                Keep This Letter Forever 💝
            </h3>
            <p style="font-family: 'Indie Flower', cursive; color: #5d4e37; font-size: 1.1rem;">
                Download your personal letter as a beautiful keepsake
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate and display the letter image
        try:
            letter_img = create_letter_image(user_name, user_data['letter'], user_data['signature'])
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(letter_img, caption="Your Personal Letter", use_container_width=True)
                
                # Create download button
                buffer = io.BytesIO()
                letter_img.save(buffer, format='PNG')
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Letter as PNG",
                    data=buffer,
                    file_name=f"letter_for_{user_name.lower()}.png",
                    mime="image/png",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error generating letter image: {str(e)}")
            st.info("You can still view your letter above, but image generation is temporarily unavailable.")
        
        # Closing message
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem;">
            <p style="font-family: 'Dancing Script', cursive; font-size: 1.5rem; color: #8b4513; font-style: italic;">
                This letter was made just for you. Keep it close. 💕
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout option (subtle)
        if st.button("← Back to Login", key="logout"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Application error: {str(e)}")
    st.info("Please refresh the page and try again.")