import streamlit as st
import sympy as sp


# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🧮",
    layout="wide"
)


# ============================================================
# CSS / TAMPILAN KOTAK
# ============================================================

st.markdown(
    """
    <style>

    /* Background utama */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Judul utama */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .main-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Kotak/card */
    .card {
        background-color: white;
        border: 1px solid #dbe2ea;
        border-radius: 15px;
        padding: 22px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }

    /* Judul card */
    .card-title {
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* Kotak hasil */
    .result-card {
        background-color: white;
        border: 2px solid #22c55e;
        border-radius: 15px;
        padding: 22px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 3px 10px rgba(34, 197, 94, 0.10);
    }

    /* Kotak langkah */
    .step-card {
        background-color: white;
        border: 1px solid #dbe2ea;
        border-left: 5px solid #6366f1;
        border-radius: 12px;
        padding: 18px;
        margin-top: 12px;
        margin-bottom: 12px;
    }

    /* Kotak informasi */
    .info-card {
        background-color: white;
        border: 1px solid #dbe2ea;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }

    /* Tombol */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    /* Input matriks */
    div[data-testid="stNumberInput"] {
        background-color: white;
        border-radius: 8px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧮 Kalkulator Matriks</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Kalkulator matriks dengan hasil dan langkah-langkah penyelesaian'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FUNGSI MEMBUAT KOTAK
# ============================================================

def buka_card(judul, kelas="card"):
    st.markdown(
        f"""
        <div class="{kelas}">
            <div class="card-title">{judul}</div>
        """,
        unsafe_allow_html=True
    )


def tutup_card():
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FUNGSI INPUT MATRIKS
# ============================================================

def input_matrix(nama, baris, kolom, prefix):

    buka_card(f"📐 Matriks {nama}")

    data = []

    for i in range(baris):

        cols = st.columns(kolom)

        row = []

        for j in range(kolom):

            nilai = cols[j].number_input(
                f"{nama}[{i+1},{j+1}]",
                value=0.0,
                step=1.0,
                format="%.2f",
                key=f"{prefix}_{i}_{j}"
            )

            nilai_sympy = sp.Rational(
                str(nilai)
            ).limit_denominator(100000)

            row.append(nilai_sympy)

        data.append(row)

    tutup_card()

    return sp.Matrix(data)


# ============================================================
# FUNGSI MENAMPILKAN MATRIKS
# ============================================================

def tampilkan_matriks(A, judul):

    buka_card(judul, "result-card")

    st.latex(
        sp.latex(A)
    )

    tutup_card()


# ============================================================
# FUNGSI LANGKAH PENJUMLAHAN
# ============================================================

def langkah_penjumlahan(A, B):

    C = A + B
    langkah = []

    for i in range(A.rows):

        for j in range(A.cols):

            a = A[i, j]
            b = B[i, j]
            c = C[i, j]

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                A_{{{i+1},{j+1}}}
                +
                B_{{{i+1},{j+1}}}
                =
                ({sp.latex(a)})
                +
                ({sp.latex(b)})
                =
                \mathbf{{{sp.latex(c)}}}
                """
            )

    return C, langkah


# ============================================================
# FUNGSI LANGKAH PENGURANGAN
# ============================================================

def langkah_pengurangan(A, B):

    C = A - B
    langkah = []

    for i in range(A.rows):

        for j in range(A.cols):

            a = A[i, j]
            b = B[i, j]
            c = C[i, j]

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                A_{{{i+1},{j+1}}}
                -
                B_{{{i+1},{j+1}}}
                =
                ({sp.latex(a)})
                -
                ({sp.latex(b)})
                =
                \mathbf{{{sp.latex(c)}}}
                """
            )

    return C, langkah


# ============================================================
# FUNGSI LANGKAH PERKALIAN
# ============================================================

def langkah_perkalian(A, B):

    C = A * B
    langkah = []

    for i in range(A.rows):

        for j in range(B.cols):

            bagian = []

            for k in range(A.cols):

                bagian.append(
                    f"({sp.latex(A[i, k])})"
                    f"({sp.latex(B[k, j])})"
                )

            persamaan = " + ".join(bagian)

            langkah.append(
                rf"""
                C_{{{i+1},{j+1}}}
                =
                {persamaan}
                =
                \mathbf{{{sp.latex(C[i, j])}}}
                """
            )

    return C, langkah


# ============================================================
# FUNGSI DETERMINAN
# ============================================================

def langkah_determinan(A):

    det = sp.simplify(A.det())
    langkah = []

    if A.rows == 1:

        langkah.append(
            rf"""
            \det(A)
            =
            {sp.latex(A[0, 0])}
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    elif A.rows == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        langkah.append(
            rf"""
            \det(A)
            =
            ({sp.latex(a)})({sp.latex(d)})
            -
            ({sp.latex(b)})({sp.latex(c)})
            """
        )

        langkah.append(
            rf"""
            =
            {sp.latex(a*d)}
            -
            {sp.latex(b*c)}
            """
        )

        langkah.append(
            rf"""
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    elif A.rows == 3:

        a = A[0, 0]
        b = A[0, 1]
        c = A[0, 2]

        d = A[1, 0]
        e = A[1, 1]
        f = A[1, 2]

        g = A[2, 0]
        h = A[2, 1]
        i = A[2, 2]

        langkah.append(
            rf"""
            \det(A)
            =
            ({sp.latex(a)})
            [({sp.latex(e)})({sp.latex(i)})
            -
            ({sp.latex(f)})({sp.latex(h)})]
            -
            ({sp.latex(b)})
            [({sp.latex(d)})({sp.latex(i)})
            -
            ({sp.latex(f)})({sp.latex(g)})]
            +
            ({sp.latex(c)})
            [({sp.latex(d)})({sp.latex(h)})
            -
            ({sp.latex(e)})({sp.latex(g)})]
            """
        )

        langkah.append(
            rf"""
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    else:

        langkah.append(
            r"""
            Matriks berukuran lebih dari 3 × 3.
            Determinan dihitung menggunakan operasi
            aljabar matriks.
            """
        )

        langkah.append(
            rf"""
            \det(A)
            =
            \mathbf{{{sp.latex(det)}}}
            """
        )

    return det, langkah


# ============================================================
# FUNGSI INVERS
# ============================================================

def langkah_invers(A):

    det = sp.simplify(A.det())

    if det == 0:

        return None, []

    invers = A.inv()
    langkah = []

    langkah.append(
        rf"""
        \det(A)
        =
        {sp.latex(det)}
        """
    )

    if A.rows == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        langkah.append(
            rf"""
            A^{{-1}}
            =
            \frac{{1}}{{\det(A)}}
            \begin{{bmatrix}}
            d & -b \\
            -c & a
            \end{{bmatrix}}
            """
        )

        langkah.append(
            rf"""
            A^{{-1}}
            =
            \frac{{1}}{{{sp.latex(det)}}}
            \begin{{bmatrix}}
            {sp.latex(d)} & -{sp.latex(b)} \\
            -{sp.latex(c)} & {sp.latex(a)}
            \end{{bmatrix}}
            """
        )

        langkah.append(
            rf"""
            A^{{-1}}
            =
            {sp.latex(invers)}
            """
        )

    else:

        augmented = A.row_join(
            sp.eye(A.rows)
        )

        rref, _ = augmented.rref()

        langkah.append(
            r"""
            Invers dihitung menggunakan metode
            Gauss-Jordan pada matriks augmented [A | I].
            """
        )

        langkah.append(
            rf"""
            [A|I]
            =
            {sp.latex(augmented)}
            """
        )

        langkah.append(
            rf"""
            RREF([A|I])
            =
            {sp.latex(rref)}
            """
        )

        langkah.append(
            rf"""
            A^{{-1}}
            =
            {sp.latex(invers)}
            """
        )

    return invers, langkah


# ============================================================
# FUNGSI RREF
# ============================================================

def rref_dengan_langkah(A):

    M = A.copy()
    langkah = []

    langkah.append(
        (
            "Matriks awal",
            M.copy()
        )
    )

    baris = 0

    for kolom in range(M.cols):

        if baris >= M.rows:
            break

        pivot = None

        for r in range(baris, M.rows):

            if M[r, kolom] != 0:

                pivot = r
                break

        if pivot is None:
            continue

        if pivot != baris:

            M.row_swap(
                pivot,
                baris
            )

            langkah.append(
                (
                    f"R{baris+1} ↔ R{pivot+1}",
                    M.copy()
                )
            )

        nilai_pivot = M[baris, kolom]

        if nilai_pivot != 1:

            M.row_op(
                baris,
                lambda nilai, j:
                sp.simplify(
                    nilai / nilai_pivot
                )
            )

            langkah.append(
                (
                    f"R{baris+1} → "
                    f"R{baris+1}/({sp.latex(nilai_pivot)})",
                    M.copy()
                )
            )

        for r in range(M.rows):

            if r == baris:
                continue

            faktor = M[r, kolom]

            if faktor != 0:

                M.row_op(
                    r,
                    lambda nilai, j:
                    sp.simplify(
                        nilai -
                        faktor * M[baris, j]
                    )
                )

                langkah.append(
                    (
                        f"R{r+1} → "
                        f"R{r+1} - "
                        f"({sp.latex(faktor)})R{baris+1}",
                        M.copy()
                    )
                )

        baris += 1

    return M, langkah


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧮 Kalkulator")

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

st.sidebar.divider()

st.sidebar.info(
    """
    **Operasi yang tersedia:**

    ➕ Penjumlahan

    ➖ Pengurangan

    ✖️ Perkalian

    🔄 Transpose

    📊 Determinan

    🔁 Invers

    📈 Rank

    Σ Trace

    📐 SPL Gauss-Jordan
    """
)


# ============================================================
# TRANSPOSE
# ============================================================

if operasi == "Transpose":

    st.header("🔄 Transpose Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="transpose_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="transpose_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "transpose"
    )

    if st.button(
        "🔢 HITUNG TRANSPOSE",
        type="primary",
        use_container_width=True
    ):

        hasil = A.T

        tampilkan_matriks(
            hasil,
            "✅ Hasil Aᵀ"
        )

        buka_card(
            "📖 Langkah Penyelesaian",
            "step-card"
        )

        st.write(
            "Transpose dilakukan dengan mengubah "
            "baris menjadi kolom."
        )

        st.latex(
            rf"A^T = {sp.latex(hasil)}"
        )

        tutup_card()


# ============================================================
# DETERMINAN
# ============================================================

elif operasi == "Determinan":

    st.header("📊 Determinan Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="det_ukuran"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "determinan"
    )

    if st.button(
        "🔢 HITUNG DETERMINAN",
        type="primary",
        use_container_width=True
    ):

        hasil, langkah = langkah_determinan(A)

        tampilkan_matriks(
            sp.Matrix([[hasil]]),
            "✅ Hasil Determinan"
        )

        buka_card(
            "📖 Langkah Penyelesaian",
            "step-card"
        )

        for nomor, item in enumerate(
            langkah,
            start=1
        ):

            st.write(
                f"**Langkah {nomor}**"
            )

            st.latex(item)

        tutup_card()


# ============================================================
# INVERS
# ============================================================

elif operasi == "Invers":

    st.header("🔁 Invers Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="inv_ukuran"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "invers"
    )

    if st.button(
        "🔢 HITUNG INVERS",
        type="primary",
        use_container_width=True
    ):

        det = sp.simplify(A.det())

        if det == 0:

            st.error(
                "Matriks tidak memiliki invers "
                "karena determinannya = 0."
            )

        else:

            hasil, langkah = langkah_invers(A)

            tampilkan_matriks(
                hasil,
                "✅ Hasil A⁻¹"
            )

            buka_card(
                "📖 Langkah Penyelesaian",
                "step-card"
            )

            for nomor, item in enumerate(
                langkah,
                start=1
            ):

                st.write(
                    f"**Langkah {nomor}**"
                )

                st.latex(item)

            tutup_card()


# ============================================================
# RANK
# ============================================================

elif operasi == "Rank":

    st.header("📈 Rank Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="rank_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=8,
            value=2,
            step=1,
            key="rank_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "rank"
    )

    if st.button(
        "🔢 HITUNG RANK",
        type="primary",
        use_container_width=True
    ):

        hasil = A.rank()

        rref, langkah = rref_dengan_langkah(A)

        buka_card(
            "✅ Hasil Rank",
            "result-card"
        )

        st.latex(
            rf"\operatorname{{rank}}(A)"
            rf" = \mathbf{{{hasil}}}"
        )

        tutup_card()

        buka_card(
            "📖 Langkah RREF",
            "step-card"
        )

        for nomor, (deskripsi, matriks) in enumerate(
            langkah,
            start=1
        ):

            st.write(
                f"**Langkah {nomor}: {deskripsi}**"
            )

            st.latex(
                sp.latex(matriks)
            )

        tutup_card()


# ============================================================
# TRACE
# ============================================================

elif operasi == "Trace":

    st.header("Σ Trace Matriks")

    ukuran = st.number_input(
        "Ukuran matriks persegi",
        min_value=1,
        max_value=8,
        value=2,
        step=1,
        key="trace_ukuran"
    )

    A = input_matrix(
        "A",
        int(ukuran),
        int(ukuran),
        "trace"
    )

    if st.button(
        "🔢 HITUNG TRACE",
        type="primary",
        use_container_width=True
    ):

        hasil = sp.trace(A)

        diagonal = []

        for i in range(A.rows):

            diagonal.append(
                sp.latex(A[i, i])
            )

        persamaan = " + ".join(diagonal)

        buka_card(
            "✅ Hasil Trace",
            "result-card"
        )

        st.latex(
            rf"\operatorname{{tr}}(A)"
            rf" = \mathbf{{{sp.latex(hasil)}}}"
        )

        tutup_card()

        buka_card(
            "📖 Langkah Penyelesaian",
            "step-card"
        )

        st.latex(
            rf"\operatorname{{tr}}(A)"
            rf" = {persamaan}"
        )

        st.latex(
            rf"= \mathbf{{{sp.latex(hasil)}}}"
        )

        tutup_card()


# ============================================================
# PENJUMLAHAN
# =====================================================
