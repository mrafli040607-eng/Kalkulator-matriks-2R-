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
# CSS TAMPILAN
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       BACKGROUND
       ========================= */

    .stApp {
        background: linear-gradient(
            135deg,
            #eef2ff 0%,
            #f8fafc 50%,
            #ecfeff 100%
        );
    }

    /* =========================
       HEADER
       ========================= */

    .header-box {
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );
        padding: 28px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.25);
    }

    .header-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .header-subtitle {
        font-size: 16px;
        opacity: 0.9;
    }

    /* =========================
       CARD
       ========================= */

    .box {
        background: white;
        border: 2px solid #dbeafe;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(15, 23, 42, 0.08);
    }

    .matrix-box {
        background: white;
        border: 3px solid #6366f1;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 7px 18px rgba(99, 102, 241, 0.15);
    }

    .result-box {
        background: #ecfdf5;
        border: 3px solid #22c55e;
        border-radius: 18px;
        padding: 25px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 7px 18px rgba(34, 197, 94, 0.15);
    }

    .step-box {
        background: #fffbeb;
        border: 3px solid #f59e0b;
        border-radius: 18px;
        padding: 22px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 7px 18px rgba(245, 158, 11, 0.12);
    }

    .info-box {
        background: #eff6ff;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
    }

    /* =========================
       JUDUL CARD
       ========================= */

    .box-title {
        font-size: 22px;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 15px;
    }

    .matrix-title {
        font-size: 22px;
        font-weight: 800;
        color: #4f46e5;
        margin-bottom: 15px;
    }

    .result-title {
        font-size: 23px;
        font-weight: 800;
        color: #15803d;
        margin-bottom: 15px;
    }

    .step-title {
        font-size: 23px;
        font-weight: 800;
        color: #b45309;
        margin-bottom: 15px;
    }

    /* =========================
       TOMBOL
       ========================= */

    div.stButton > button {
        width: 100%;
        min-height: 50px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 800;
        border: none;
    }

    /* =========================
       INPUT
       ========================= */

    div[data-testid="stNumberInput"] {
        background: white;
        border-radius: 10px;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #1e1b4b,
            #312e81
        );
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #64748b;
        padding: 25px;
        font-size: 14px;
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
    <div class="header-box">
        <div class="header-title">
            🧮 KALKULATOR MATRIKS
        </div>
        <div class="header-subtitle">
            Perhitungan matriks lengkap dengan langkah penyelesaian
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNGSI CARD
# =========================================================

def card(judul, jenis="box"):

    st.markdown(
        f"""
        <div class="{jenis}">
            <div class="box-title">
                {judul}
            </div>
        """,
        unsafe_allow_html=True
    )


def end_card():

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# INPUT MATRIKS
# =========================================================

def input_matrix(nama, baris, kolom, prefix):

    st.markdown(
        f"""
        <div class="matrix-box">
            <div class="matrix-title">
                📐 MATRIKS {nama}
            </div>
        """,
        unsafe_allow_html=True
    )

    data = []

    for i in range(baris):

        kolom_input = st.columns(kolom)

        row = []

        for j in range(kolom):

            nilai = kolom_input[j].number_input(
                f"{nama}[{i+1},{j+1}]",
                value=0.0,
                step=1.0,
                format="%.2f",
                key=f"{prefix}_{i}_{j}"
            )

            nilai = sp.Rational(
                str(nilai)
            ).limit_denominator(100000)

            row.append(nilai)

        data.append(row)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    return sp.Matrix(data)


# =========================================================
# TAMPILKAN HASIL
# =========================================================

def tampilkan_hasil(judul, matriks):

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                {judul}
            </div>
        """,
        unsafe_allow_html=True
    )

    st.latex(
        sp.latex(matriks)
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# TAMPILKAN LANGKAH
# =========================================================

def tampilkan_langkah(judul, langkah):

    st.markdown(
        f"""
        <div class="step-box">
            <div class="step-title">
                {judul}
            </div>
        """,
        unsafe_allow_html=True
    )

    for nomor, langkah_satu in enumerate(
        langkah,
        start=1
    ):

        st.markdown(
            f"**Langkah {nomor}**"
        )

        st.latex(langkah_satu)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        font-size:28px;
        font-weight:800;
        margin-bottom:20px;
    ">
        🧮 MENU
    </div>
    """,
    unsafe_allow_html=True
)

operasi = st.sidebar.selectbox(
    "Pilih Operasi",
    [
        "Penjumlahan",
        "Pengurangan",
        "Perkalian",
        "Transpose",
        "Determinan",
        "Invers",
        "Rank",
        "Trace",
        "SPL - Gauss-Jordan"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    ### 📚 Operasi

    ➕ Penjumlahan

    ➖ Pengurangan

    ✖️ Perkalian

    🔄 Transpose

    📊 Determinan

    🔁 Invers

    📈 Rank

    Σ Trace

    📐 SPL
    """
)


# =========================================================
# PENJUMLAHAN
# =========================================================

if operasi == "Penjumlahan":

    st.subheader("➕ Penjumlahan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        card("Ukuran Matriks A")

        baris_a = st.number_input(
            "Jumlah baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="add_ra"
        )

        kolom_a = st.number_input(
            "Jumlah kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="add_ka"
        )

        end_card()

    with col2:

        card("Ukuran Matriks B")

        baris_b = st.number_input(
            "Jumlah baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="add_rb"
        )

        kolom_b = st.number_input(
            "Jumlah kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="add_kb"
        )

        end_card()

    col1, col2 = st.columns(2)

    with col1:

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "add_A"
        )

    with col2:

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "add_B"
        )

    if st.button(
        "➕ HITUNG A + B",
        type="primary"
    ):

        if A.shape != B.shape:

            st.error(
                "❌ Ukuran Matriks A dan B harus sama."
            )

        else:

            C = A + B

            tampilkan_hasil(
                "🟢 HASIL A + B",
                C
            )

            langkah = []

            for i in range(A.rows):

                for j in range(A.cols):

                    langkah.append(
                        rf"""
                        C_{{{i+1},{j+1}}}
                        =
                        A_{{{i+1},{j+1}}}
                        +
                        B_{{{i+1},{j+1}}}
                        =
                        {sp.latex(A[i,j])}
                        +
                        {sp.latex(B[i,j])}
                        =
                        \mathbf{{{sp.latex(C[i,j])}}}
                        """
                    )

            tampilkan_langkah(
                "📖 LANGKAH PENJUMLAHAN",
                langkah
            )


# =========================================================
# PENGURANGAN
# =========================================================

elif operasi == "Pengurangan":

    st.subheader("➖ Pengurangan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        card("Ukuran Matriks A")

        baris_a = st.number_input(
            "Jumlah baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="sub_ra"
        )

        kolom_a = st.number_input(
            "Jumlah kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="sub_ka"
        )

        end_card()

    with col2:

        card("Ukuran Matriks B")

        baris_b = st.number_input(
            "Jumlah baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="sub_rb"
        )

        kolom_b = st.number_input(
            "Jumlah kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="sub_kb"
        )

        end_card()

    col1, col2 = st.columns(2)

    with col1:

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "sub_A"
        )

    with col2:

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "sub_B"
        )

    if st.button(
        "➖ HITUNG A - B",
        type="primary"
    ):

        if A.shape != B.shape:

            st.error(
                "❌ Ukuran Matriks A dan B harus sama."
            )

        else:

            C = A - B

            tampilkan_hasil(
                "🟢 HASIL A - B",
                C
            )

            langkah = []

            for i in range(A.rows):

                for j in range(A.cols):

                    langkah.append(
                        rf"""
                        C_{{{i+1},{j+1}}}
                        =
                        A_{{{i+1},{j+1}}}
                        -
                        B_{{{i+1},{j+1}}}
                        =
                        {sp.latex(A[i,j])}
                        -
                        {sp.latex(B[i,j])}
                        =
                        \mathbf{{{sp.latex(C[i,j])}}}
                        """
                    )

            tampilkan_langkah(
                "📖 LANGKAH PENGURANGAN",
                langkah
            )


# =========================================================
# PERKALIAN
# =========================================================

elif operasi == "Perkalian":

    st.subheader("✖️ Perkalian Matriks")

    col1, col2 = st.columns(2)

    with col1:

        card("Ukuran Matriks A")

        baris_a = st.number_input(
            "Jumlah baris A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="mul_ra"
        )

        kolom_a = st.number_input(
            "Jumlah kolom A",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="mul_ka"
        )

        end_card()

    with col2:

        card("Ukuran Matriks B")

        baris_b = st.number_input(
            "Jumlah baris B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="mul_rb"
        )

        kolom_b = st.number_input(
            "Jumlah kolom B",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="mul_kb"
        )

        end_card()

    col1, col2 = st.columns(2)

    with col1:

        A = input_matrix(
            "A",
            int(baris_a),
            int(kolom_a),
            "mul_A"
        )

    with col2:

        B = input_matrix(
            "B",
            int(baris_b),
            int(kolom_b),
            "mul_B"
        )

    if st.button(
        "✖️ HITUNG A × B",
        type="primary"
    ):

        if A.cols != B.rows:

            st.error(
                "❌ Perkalian tidak dapat dilakukan."
            )

            st.info(
                "Jumlah kolom A harus sama "
                "dengan jumlah baris B."
            )

        else:

            C = A * B

            tampilkan_hasil(
                "🟢 HASIL A × B",
                C
            )

            langkah = []

            for i in range(C.rows):

                for j in range(C.cols):

                    bagian = []

                    for k in range(A.cols):

                        bagian.append(
                            f"({sp.latex(A[i,k])})"
                            f"({sp.latex(B[k,j])})"
                        )

                    persamaan = " + ".join(bagian)

                    langkah.append(
                        rf"""
                        C_{{{i+1},{j+1}}}
                        =
                        {persamaan}
                        =
                        \mathbf{{{sp.latex(C[i,j])}}}
                        """
                    )

            tampilkan_langkah(
                "📖 LANGKAH PERKALIAN",
                langkah
            )


# =========================================================
# TRANSPOSE
# =========================================================

elif operasi == "Transpose":

    st.subheader("🔄 Transpose Matriks")

    col1, col2 = st.columns(2)

    with col1:

        card("Ukuran Matriks")

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="trans_r"
        )

        end_card()

    with col2:

        card("Ukuran Matriks")

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="trans_k"
        )

        end_card()

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "trans_A"
    )

    if st.button(
        "🔄 HITUNG TRANSPOSE",
        type="primary"
    ):

        C = A.T

        tampilkan_hasil(
            "🟢 HASIL Aᵀ",
            C
        )

        tampilkan_langkah(
            "📖 LANGKAH TRANSPOSE",
            [
                rf"""
                A =
                {sp.latex(A)}
                """,
                rf"""
                A^T =
                {sp.latex(C)}
                """
            ]
        )


# =========================================================
# DETERMINAN
# =========================================================

elif operasi == "Determinan":

    st.subheader("📊 Determinan Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="det_n"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "det_A"
    )

    if st.button(
        "📊 HITUNG DETERMINAN",
        type="primary"
    ):

        hasil = sp.simplify(A.det())

        tampilkan_hasil(
            "🟢 HASIL DETERMINAN",
            sp.Matrix([[hasil]])
        )

        langkah = []

        if A.rows == 2:

            a = A[0, 0]
            b = A[0, 1]
            c = A[1, 0]
            d = A[1, 1]

            langkah.append(
                rf"""
                \det(A)
                =
                ({sp.latex(a)})
                ({sp.latex(d)})
                -
                ({sp.latex(b)})
                ({sp.latex(c)})
                """
            )

            langkah.append(
                rf"""
                =
                {sp.latex(a*d)}
                -
                {sp.latex(b*c)}
                =
                \mathbf{{{sp.latex(hasil)}}}
                """
            )

        else:

            langkah.append(
                rf"""
                \det(A)
                =
                \mathbf{{{sp.latex(hasil)}}}
                """
            )

        tampilkan_langkah(
            "📖 LANGKAH DETERMINAN",
            langkah
        )


# =========================================================
# INVERS
# =========================================================

elif operasi == "Invers":

    st.subheader("🔁 Invers Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="inv_n"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "inv_A"
    )

    if st.button(
        "🔁 HITUNG INVERS",
        type="primary"
    ):

        det = sp.simplify(A.det())

        if det == 0:

            st.error(
                "❌ Matriks tidak memiliki invers "
                "karena determinannya = 0."
            )

        else:

            C = A.inv()

            tampilkan_hasil(
                "🟢 HASIL A⁻¹",
                C
            )

            langkah = [
                rf"""
                \det(A)
                =
                {sp.latex(det)}
                """,
                rf"""
                A^{{-1}}
                =
                {sp.latex(C)}
                """
            ]

            tampilkan_langkah(
                "📖 LANGKAH INVERS",
                langkah
            )


# ========================================
