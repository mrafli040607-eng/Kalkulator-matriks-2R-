import streamlit as st
import sympy as sp


# =========================================================
# KONFIGURASI
# =========================================================

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🧮",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    .header {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }

    .header h1 {
        margin: 0;
        font-size: 35px;
    }

    .header p {
        margin: 8px 0 0 0;
        font-size: 16px;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.07);
    }

    .matrix-title {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #4f46e5;
        margin-bottom: 12px;
    }

    /* Kotak setiap elemen matriks */
    div[data-testid="stNumberInput"] {
        background-color: white !important;
        border: 2px solid #6366f1 !important;
        border-radius: 7px !important;
        padding: 2px !important;
        margin-bottom: 5px !important;
    }

    div[data-testid="stNumberInput"]:focus-within {
        border-color: #312e81 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
    }

    div[data-testid="stNumberInput"] input {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #111827 !important;
    }

    .result-box {
        background-color: #eef2ff;
        border-left: 5px solid #4f46e5;
        padding: 18px;
        border-radius: 10px;
        margin-top: 20px;
    }

    .step-box {
        background-color: white;
        border: 1px solid #d1d5db;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        padding: 30px;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="header">
        <h1>🧮 Kalkulator Matriks</h1>
        <p>Perhitungan matriks menggunakan Python dan Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNGSI INPUT MATRIKS
# =========================================================

def input_matrix(nama, baris, kolom, prefix):

    st.markdown(
        f'<div class="matrix-title">Matriks {nama}</div>',
        unsafe_allow_html=True
    )

    data = []

    for i in range(baris):

        columns = st.columns(kolom, gap="small")

        row = []

        for j in range(kolom):

            with columns[j]:

                nilai = st.number_input(
                    f"{nama}[{i+1},{j+1}]",
                    value=0.0,
                    step=1.0,
                    format="%.0f",
                    key=f"{prefix}_{i}_{j}",
                    label_visibility="collapsed"
                )

                row.append(
                    sp.Rational(
                        str(nilai)
                    ).limit_denominator(100000)
                )

        data.append(row)

    return sp.Matrix(data)


# =========================================================
# FUNGSI MENAMPILKAN HASIL
# =========================================================

def tampilkan_hasil(judul, hasil):

    st.markdown(
        f"""
        <div class="result-box">
            <h3>{judul}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.latex(sp.latex(hasil))


# =========================================================
# FUNGSI LANGKAH
# =========================================================

def tampilkan_langkah(teks):

    st.markdown(
        f"""
        <div class="step-box">
            <b>📌 Langkah:</b><br>
            {teks}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Menu Operasi")

operasi = st.sidebar.selectbox(
    "Pilih operasi:",
    [
        "Penjumlahan",
        "Pengurangan",
        "Perkalian",
        "Transpose",
        "Determinan",
        "Invers",
        "Rank",
        "Trace",
        "SPL Gauss-Jordan"
    ]
)


# =========================================================
# PENJUMLAHAN
# =========================================================

if operasi == "Penjumlahan":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("➕ Penjumlahan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            key="tambah_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            key="tambah_kolom"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        A = input_matrix(
            "A",
            int(baris),
            int(kolom),
            "tambah_A"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        B = input_matrix(
            "B",
            int(baris),
            int(kolom),
            "tambah_B"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🧮 Hitung A + B",
        use_container_width=True
    ):

        hasil = A + B

        tampilkan_hasil(
            "Hasil A + B",
            hasil
        )

        tampilkan_langkah(
            "Elemen yang memiliki posisi sama dijumlahkan."
        )


# =========================================================
# PENGURANGAN
# =========================================================

elif operasi == "Pengurangan":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("➖ Pengurangan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            key="kurang_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            key="kurang_kolom"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        A = input_matrix(
            "A",
            int(baris),
            int(kolom),
            "kurang_A"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        B = input_matrix(
            "B",
            int(baris),
            int(kolom),
            "kurang_B"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🧮 Hitung A − B",
        use_container_width=True
    ):

        hasil = A - B

        tampilkan_hasil(
            "Hasil A − B",
            hasil
        )

        tampilkan_langkah(
            "Elemen matriks B dikurangkan dari elemen matriks A "
            "yang berada pada posisi yang sama."
        )


# =========================================================
# PERKALIAN
# =========================================================

elif operasi == "Perkalian":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("✖️ Perkalian Matriks")

    st.markdown("### Ukuran Matriks A")

    col1, col2 = st.columns(2)

    with col1:

        baris_A = st.number_input(
            "Baris A",
            min_value=1,
            max_value=8,
            value=2,
            key="kali_baris_A"
        )

    with col2:

        kolom_A = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=8,
            value=2,
            key="kali_kolom_A"
        )

    st.markdown("### Ukuran Matriks B")

    col1, col2 = st.columns(2)

    with col1:

        baris_B = st.number_input(
            "Baris B",
            min_value=1,
            max_value=8,
            value=2,
            key="kali_baris_B"
        )

    with col2:

        kolom_B = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=8,
            value=2,
            key="kali_kolom_B"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if int(kolom_A) != int(baris_B):

        st.warning(
            "⚠️ Jumlah kolom Matriks A harus sama "
            "dengan jumlah baris Matriks B."
        )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        A = input_matrix(
            "A",
            int(baris_A),
            int(kolom_A),
            "kali_A"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        B = input_matrix(
            "B",
            int(baris_B),
            int(kolom_B),
            "kali_B"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🧮 Hitung A × B",
        use_container_width=True
    ):

        if int(kolom_A) != int(baris_B):

            st.error(
                "Perkalian tidak dapat dilakukan karena "
                "ukuran matriks tidak memenuhi syarat."
            )

        else:

            hasil = A * B

            tampilkan_hasil(
                "Hasil A × B",
                hasil
            )

            tampilkan_langkah(
                "Setiap elemen hasil diperoleh dari perkalian "
                "baris Matriks A dengan kolom Matriks B."
            )


# =========================================================
# TRANSPOSE
# =========================================================

elif operasi == "Transpose":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("🔄 Transpose Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            key="transpose_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=3,
            key="transpose_kolom"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "transpose_A"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🔄 Hitung Transpose",
        use_container_width=True
    ):

        hasil = A.T

        tampilkan_hasil(
            "Transpose Matriks A",
            hasil
        )

        tampilkan_langkah(
            "Transpose dilakukan dengan mengubah setiap baris "
            "menjadi kolom."
        )


# =========================================================
# DETERMINAN
# =========================================================

elif operasi == "Determinan":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("📐 Determinan Matriks")

    ukuran = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=8,
        value=2,
        key="determinan_ukuran"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "determinan_A"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "📐 Hitung Determinan",
        use_container_width=True
    ):

        hasil = A.det()

        tampilkan_hasil(
            "Determinan A",
            hasil
        )

        tampilkan_langkah(
            "Determinan dihitung berdasarkan elemen-elemen "
            "matriks persegi."
        )


# =========================================================
# INVERS
# =========================================================

elif operasi == "Invers":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("🔁 Invers Matriks")

    ukuran = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=8,
        value=2,
        key="invers_ukuran"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "invers_A"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🔁 Hitung Invers",
        use_container_width=True
    ):

        if A.det() == 0:

            st.error(
                "Matriks tidak mempunyai invers karena "
                "determinan = 0."
            )

        else:

            hasil = A.inv()

            tampilkan_hasil(
                "Invers Matriks A",
                hasil
            )

            tampilkan_langkah(
                "Syarat matriks mempunyai invers adalah "
                "determinan matriks tidak sama dengan nol."
            )


# =========================================================
# RANK
# =========================================================

elif operasi == "Rank":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("📊 Rank Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            key="rank_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            key="rank_kolom"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "rank_A"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "📊 Hitung Rank",
        use_container_width=True
    ):

        hasil = A.rank()

        tampilkan_hasil(
            "Rank Matriks A",
            hasil
        )

        tampilkan_langkah(
            "Rank menunjukkan jumlah maksimum baris atau kolom "
            "yang independen secara linear."
        )


# =========================================================
# TRACE
# =========================================================

elif operasi == "Trace":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("Σ Trace Matriks")

    ukuran = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=8,
        value=3,
        key="trace_ukuran"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "trace_A"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "Σ Hitung Trace",
        use_container_width=True
    ):

        hasil = A.trace()

        tampilkan_hasil(
            "Trace Matriks A",
            hasil
        )

        tampilkan_langkah(
            "Trace adalah jumlah elemen pada diagonal utama matriks."
        )


# =========================================================
# SPL GAUSS-JORDAN
# =========================================================

elif operasi == "SPL Gauss-Jordan":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("📚 Sistem Persamaan Linear")

    jumlah = st.number_input(
        "Jumlah persamaan / variabel",
        min_value=1,
        max_value=8,
        value=2,
        key="spl_jumlah"
    )

    st.info(
        "Masukkan matriks augmented. "
        "Contoh 2x + 3y = 7 dimasukkan sebagai 2, 3, 7."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    A = input_matrix(
        "Augmented",
        int(jumlah),
        int(jumlah) + 1,
        "spl_A"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "📚 Selesaikan SPL",
        use_container_width=True
    ):

        rref_matrix, pivot_columns = A.rref()

        tampilkan_hasil(
            "Hasil Gauss-Jordan / RREF",
            rref_matrix
        )

        tampilkan_langkah(
            "Operasi baris elementer dilakukan sampai matriks "
            "mencapai bentuk Reduced Row Echelon Form (RREF)."
        )

        # Cek apakah ada baris kontradiksi
        ada_kontradiksi = False

        for i in range(rref_matrix.rows):

            semua_nol = True

            for j in range(int(jumlah)):

                if rref_matrix[i, j] != 0:

                    semua_nol = False
                    break

            konstanta = rref_matrix[i, int(jumlah)]

            if semua_nol and konstanta != 0:

                ada_kontradiksi = True

        if ada_kontradiksi:

            st.error(
                "SPL tidak memiliki solusi."
            )

        elif len(pivot_columns) == int(jumlah):

            st.success(
                "SPL memiliki solusi tunggal."
            )

            for i in range(int(jumlah)):

                nilai = rref_matrix[i, int(jumlah)]

                st.latex(
                    f"x_{{{i+1}}} = {sp.latex(nilai)}"
                )

        else:

            st.warning(
                "SPL memiliki variabel bebas atau "
                "memiliki banyak solusi."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🧮 Kalkulator Matriks
        <br>
        Python • Streamlit • SymPy
    </div>
    """,
    unsafe_allow_html=True
        )
