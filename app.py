import streamlit as st
import sympy as sp


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🔢",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .judul {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        color: #4F46E5;
        margin-bottom: 5px;
    }

    .subjudul {
        text-align: center;
        color: #6B7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .judul-matriks {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        color: #4F46E5;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    div[data-testid="stNumberInput"] {
        background-color: white !important;
        border: 2px solid #4F46E5 !important;
        border-radius: 8px !important;
        padding: 2px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
    }

    div[data-testid="stNumberInput"]:focus-within {
        border: 2px solid #312E81 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
    }

    div[data-testid="stNumberInput"] input {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #111827 !important;
        height: 42px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# JUDUL
# =========================================================

st.markdown(
    '<div class="judul">🔢 KALKULATOR MATRIKS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subjudul">'
    'Perhitungan matriks lengkap dengan langkah-langkah penyelesaian'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# FUNGSI INPUT MATRIKS
# =========================================================

def input_matrix(nama, baris, kolom, prefix):

    data = []

    st.markdown(
        f"""
        <div class="judul-matriks">
            Matriks {nama}
        </div>
        """,
        unsafe_allow_html=True
    )

    for i in range(baris):

        kolom_input = st.columns(
            kolom,
            gap="small"
        )

        baris_data = []

        for j in range(kolom):

            with kolom_input[j]:

                nilai = st.number_input(
                    f"{nama}[{i+1},{j+1}]",
                    value=0.0,
                    step=1.0,
                    format="%.4f",
                    key=f"{prefix}_{i}_{j}",
                    label_visibility="collapsed"
                )

                nilai_sympy = sp.Rational(
                    str(nilai)
                ).limit_denominator(100000)

                baris_data.append(
                    nilai_sympy
                )

        data.append(baris_data)

    return sp.Matrix(data)


# =========================================================
# PENJUMLAHAN
# =========================================================

def langkah_penjumlahan(A, B):

    C = A + B

    st.markdown("### Langkah Penjumlahan")

    st.latex(
        r"A+B="
        + sp.latex(A)
        + "+"
        + sp.latex(B)
    )

    st.latex(
        r"="
        + sp.latex(C)
    )

    return C


# =========================================================
# PENGURANGAN
# =========================================================

def langkah_pengurangan(A, B):

    C = A - B

    st.markdown("### Langkah Pengurangan")

    st.latex(
        r"A-B="
        + sp.latex(A)
        + "-"
        + sp.latex(B)
    )

    st.latex(
        r"="
        + sp.latex(C)
    )

    return C


# =========================================================
# PERKALIAN
# =========================================================

def langkah_perkalian(A, B):

    C = A * B

    st.markdown("### Langkah Perkalian")

    st.latex(
        r"A\times B="
        + sp.latex(A)
        + r"\times"
        + sp.latex(B)
    )

    st.latex(
        r"="
        + sp.latex(C)
    )

    st.markdown("#### Perhitungan setiap elemen:")

    for i in range(A.rows):

        for j in range(B.cols):

            suku = []

            for k in range(A.cols):

                suku.append(
                    f"({sp.latex(A[i, k])})"
                    f"({sp.latex(B[k, j])})"
                )

            persamaan = (
                f"C_{{{i+1},{j+1}}}="
                + "+".join(suku)
                + f"={sp.latex(C[i, j])}"
            )

            st.latex(persamaan)

    return C


# =========================================================
# DETERMINAN
# =========================================================

def langkah_determinan(A):

    st.markdown("### Langkah Determinan")

    if A.rows != A.cols:

        st.error(
            "Determinan hanya dapat dihitung "
            "untuk matriks persegi."
        )

        return None

    n = A.rows

    if n == 1:

        det = A[0, 0]

        st.latex(
            r"\det(A)=" + sp.latex(det)
        )

    elif n == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        det = A.det()

        st.latex(
            r"\det(A)=ad-bc"
        )

        st.latex(
            rf"""
            =({sp.latex(a)})({sp.latex(d)})
            -
            ({sp.latex(b)})({sp.latex(c)})
            """
        )

        st.latex(
            r"=" + sp.latex(det)
        )

    elif n == 3:

        a = A[0, 0]
        b = A[0, 1]
        c = A[0, 2]

        d = A[1, 0]
        e = A[1, 1]
        f = A[1, 2]

        g = A[2, 0]
        h = A[2, 1]
        i = A[2, 2]

        st.latex(
            r"""
            \det(A)
            =
            a(ei-fh)-b(di-fg)+c(dh-eg)
            """
        )

        st.latex(
            rf"""
            =
            ({sp.latex(a)})
            [({sp.latex(e)})({sp.latex(i)})
            -({sp.latex(f)})({sp.latex(h)})]
            -
            ({sp.latex(b)})
            [({sp.latex(d)})({sp.latex(i)})
            -({sp.latex(f)})({sp.latex(g)})]
            +
            ({sp.latex(c)})
            [({sp.latex(d)})({sp.latex(h)})
            -({sp.latex(e)})({sp.latex(g)})]
            """
        )

        det = A.det()

        st.latex(
            r"=" + sp.latex(det)
        )

    else:

        det = A.det()

        st.latex(
            r"\det(A)=" + sp.latex(det)
        )

        st.info(
            "Untuk matriks lebih dari 3×3, "
            "determinan dihitung menggunakan SymPy."
        )

    return det


# =========================================================
# INVERS
# =========================================================

def langkah_invers(A):

    st.markdown("### Langkah Invers")

    if A.rows != A.cols:

        st.error(
            "Invers hanya dapat dihitung "
            "untuk matriks persegi."
        )

        return None

    det = A.det()

    if det == 0:

        st.error(
            "Matriks tidak memiliki invers "
            "karena determinannya = 0."
        )

        return None

    if A.rows == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        st.latex(
            r"""
            A^{-1}
            =
            \frac{1}{ad-bc}
            \begin{bmatrix}
            d & -b\\
            -c & a
            \end{bmatrix}
            """
        )

        st.latex(
            rf"""
            \det(A)
            =
            ({sp.latex(a)})({sp.latex(d)})
            -
            ({sp.latex(b)})({sp.latex(c)})
            =
            {sp.latex(det)}
            """
        )

    else:

        st.latex(
            r"""
            A^{-1}
            =
            \frac{1}{\det(A)}
            \operatorname{adj}(A)
            """
        )

        st.latex(
            r"\det(A)=" + sp.latex(det)
        )

    inv = A.inv()

    st.markdown("#### Hasil Invers")

    st.latex(
        r"A^{-1}="
        + sp.latex(inv)
    )

    return inv


# =========================================================
# RANK
# =========================================================

def langkah_rank(A):

    st.markdown("### Rank Matriks")

    rank = A.rank()

    st.latex(
        r"\operatorname{rank}(A)="
        + str(rank)
    )

    return rank


# =========================================================
# TRACE
# =========================================================

def langkah_trace(A):

    st.markdown("### Trace Matriks")

    if A.rows != A.cols:

        st.error(
            "Trace hanya dapat dihitung "
            "untuk matriks persegi."
        )

        return None

    diagonal = []

    for i in range(A.rows):

        diagonal.append(
            A[i, i]
        )

    st.latex(
        r"""
        \operatorname{Tr}(A)
        =
        a_{11}+a_{22}+\cdots+a_{nn}
        """
    )

    st.latex(
        r"\operatorname{Tr}(A)="
        + "+".join(
            sp.latex(x)
            for x in diagonal
        )
    )

    trace = A.trace()

    st.latex(
        r"=" + sp.latex(trace)
    )

    return trace


# =========================================================
# RREF / GAUSS-JORDAN
# =========================================================

def rref_dengan_langkah(M):

    M = M.copy()

    langkah = []

    baris = M.rows
    kolom = M.cols

    pivot_row = 0

    for col in range(kolom):

        if pivot_row >= baris:

            break

        pivot = None

        for r in range(
            pivot_row,
            baris
        ):

            if M[r, col] != 0:

                pivot = r

                break

        if pivot is None:

            continue

        if pivot != pivot_row:

            M.row_swap(
                pivot,
                pivot_row
            )

            langkah.append(
                f"R{pivot_row + 1} ↔ "
                f"R{pivot + 1}"
            )

        pivot_value = M[
            pivot_row,
            col
        ]

        if pivot_value != 1:

            M.row_op(
                pivot_row,
                lambda v, j:
                v / pivot_value
            )

            langkah.append(
                f"R{pivot_row + 1} → "
                f"R{pivot_row + 1}/"
                f"({sp.latex(pivot_value)})"
            )

        for r in range(baris):

            if r == pivot_row:

                continue

            faktor = M[
                r,
                col
            ]

            if faktor != 0:

                M.row_op(
                    r,
                    lambda v, j:
                    v - faktor * M[
                        pivot_row,
                        j
                    ]
                )

                tanda = "+"

                if faktor > 0:

                    tanda = "-"

                nilai = abs(faktor)

                langkah.append(
                    f"R{r + 1} → "
                    f"R{r + 1} {tanda} "
                    f"{sp.latex(nilai)}"
                    f"R{pivot_row + 1}"
                )

        pivot_row += 1

    return M, langkah


# =========================================================
# MENAMPILKAN SPL
# =========================================================

def tampilkan_spl(A, b):

    st.markdown(
        "### Sistem Persamaan Linear"
    )

    jumlah_persamaan = A.rows
    jumlah_variabel = A.cols

    for i in range(
        jumlah_persamaan
    ):

        suku = []

        for j in range(
            jumlah_variabel
        ):

            nilai = A[i, j]

            if nilai == 0:

                continue

            if j == 0:

                suku.append(
                    f"{sp.latex(nilai)}x_1"
                )

            else:

                if nilai >= 0:

                    suku.append(
                        f"+{sp.latex(nilai)}x_{j + 1}"
                    )

                else:

                    suku.append(
                        f"{sp.latex(nilai)}x_{j + 1}"
                    )

        persamaan = "".join(suku)

        st.latex(
            persamaan
            + "="
            + sp.latex(b[i])
        )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Pengaturan")

operasi = st.sidebar.selectbox(
    "Pilih operasi:",
    [
        "Transpose",
        "Determinan",
        "Invers",
        "Rank",
        "Trace",
        "Penjumlahan",
        "Pengurangan",
        "Perkalian",
        "SPL - Gauss-Jordan"
    ]
)


# =========================================================
# TRANSPOSE
# =========================================================

if operasi == "Transpose":

    st.header("🔄 Transpose Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=10,
            value=2,
            key="transpose_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=10,
            value=2,
            key="transpose_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "transpose"
    )

    if st.button(
        "Hitung Transpose",
        key="btn_transpose"
    ):

        hasil = A.T

        st.subheader("Hasil")

        st.latex(
            r"A^T="
            + sp.latex(hasil)
        )


# =========================================================
# DETERMINAN
# =========================================================

elif operasi == "Determinan":

    st.header("📐 Determinan Matriks")

    n = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=10,
        value=3,
        key="det_n"
    )

    A = input_matrix(
        "A",
        int(n),
        int(n),
        "determinan"
    )

    if st.button(
        "Hitung Determinan",
        key="btn_determinan"
    ):

        det = langkah_determinan(A)

        if det is not None:

            st.success(
                f"Determinan = {det}"
            )


# =========================================================
# INVERS
# =========================================================

elif operasi == "Invers":

    st.header("🔁 Invers Matriks")

    n = st.number_input(
        "Ukuran matriks",
        min_value=2,
        max_value=10,
        value=2,
        key="invers_n"
    )

    A = input_matrix(
        "A",
        int(n),
        int(n),
        "invers"
    )

    if st.button(
        "Hitung Invers",
        key="btn_invers"
    ):

        langkah_invers(A)


# =========================================================
# RANK
# =========================================================

elif operasi == "Rank":

    st.header("📊 Rank Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=10,
            value=2,
            key="rank_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=10,
            value=2,
            key="rank_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "rank"
    )

    if st.button(
        "Hitung Rank",
        key="btn_rank"
    ):

        langkah_rank(A)


# =========================================================
# TRACE
# =========================================================

elif operasi == "Trace":

    st.header("🔍 Trace Matriks")

    n = st.number_input(
        "Ukuran matriks",
        min_value=1,
        max_value=10,
        value=3,
        key="trace_n"
    )

    A = input_matrix(
        "A",
        int(n),
        int(n),
        "trace"
    )

    if st.button(
        "Hitung Trace",
        key="btn_trace"
    ):

        trace = langkah_trace(A)

        if trace is not None:

            st.success(
                f"Trace = {trace}"
            )


# =========================================================
# PENJUMLAHAN
# =========================================================

elif operasi == "Penjumlahan":

    st.header("➕ Penjumlahan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=10,
            value=2,
            key="tambah_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=10,
            value=2,
            key="tambah_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "tambah_A"
    )

    B = input_matrix(
        "B",
        int(baris),
        int(kolom),
        "tambah_B"
    )

    if st.button(
        "Hitung A + B",
        key="btn_tambah"
    ):

        langkah_penjumlahan(
            A,
            B
        )


# =========================================================
# PENGURANGAN
# =========================================================

elif operasi == "Pengurangan":

    st.header("➖ Pengurangan Matriks")

    col1, col2 = st.columns(2)

    with col1:

        baris = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=10,
            value=2,
            key="kurang_baris"
        )

    with col2:

        kolom = st.number_input(
            "Jumlah kolom",
            min_value=1,
            max_value=10,
            value=2,
            key="kurang_kolom"
        )

    A = input_matrix(
        "A",
        int(baris),
        int(kolom),
        "kurang_A"
    )

    B = input_matrix(
        "B",
        int(baris),
        int(kolom),
        "kurang_B"
    )

    if st.button(
        "Hitung A - B",
        key="btn_kurang"
    ):

        langkah_pengurangan(
            A,
            B
        )


# =========================================================
# PERKALIAN
# =========================================================

elif operasi == "Perkalian":

    st.header("✖️ Perkalian Matriks")

    st.info(
        "Syarat perkalian: "
        "jumlah kolom Matriks A harus sama "
        "dengan jumlah baris Matriks B."
    )

    st.subheader("Ukuran Matriks A")

    col1, col2 = st.columns(2)

    with col1:

        baris_A = st.number_input(
            "Baris A",
            min_value=1,
            max_value=10,
            value=2,
            key="kali_baris_A"
        )

    with col2:

        kolom_A = st.number_input(
            "Kolom A",
            min_value=1,
            max_value=10,
            value=2,
            key="kali_kolom_A"
        )

    st.subheader("Ukuran Matriks B")

    col1, col2 = st.columns(2)

    with col1:

        baris_B = st.number_input(
            "Baris B",
            min_value=1,
            max_value=10,
            value=2,
            key="kali_baris_B"
        )

    with col2:

        kolom_B = st.number_input(
            "Kolom B",
            min_value=1,
            max_value=10,
            value=2,
            key="kali_kolom_B"
        )

    A = input_matrix(
        "A",
        int(baris_A),
        int(kolom_A),
        "kali_A"
    )

    B = input_matrix(
        "B",
        int(baris_B),
        int(kolom_B),
        "kali_B"
    )

    if st.button(
        "Hitung A × B",
        key="btn_kali"
    ):
        # =================================================
        # SYARAT PERKALIAN
        # =================================================

        if int(kolom_A) != int(baris_B):

            st.error(
                "Perkalian tidak dapat dilakukan!"
            )

            st.warning(
                "Jumlah kolom A harus sama "
                "dengan jumlah baris B."
            )

            st.write(
                f"Kolom A = {int(kolom_A)}"
            )

            st.write(
                f"Baris B = {int(baris_B)}"
            )

        else:

            langkah_perkalian(
                A,
                B
            )


# =========================================================
# SPL GAUSS-JORDAN
# =========================================================

elif operasi == "SPL - Gauss-Jordan":

    st.header(
        "🧮 Sistem Persamaan Linear - Gauss-Jordan"
    )

    jumlah_persamaan = st.number_input(
        "Jumlah persamaan",
        min_value=1,
        max_value=10,
        value=3,
        key="spl_jumlah_persamaan"
    )

    jumlah_variabel = st.number_input(
        "Jumlah variabel",
        min_value=1,
        max_value=10,
        value=3,
        key="spl_jumlah_variabel"
    )

    A = input_matrix(
        "A",
        int(jumlah_persamaan),
        int(jumlah_variabel),
        "spl_A"
    )

    st.markdown(
        '<div class="judul-matriks">'
        'Konstanta b'
        '</div>',
        unsafe_allow_html=True
    )

    b_data = []

    for i in range(
        int(jumlah_persamaan)
    ):

        nilai_b = st.number_input(
            f"b[{i + 1}]",
            value=0.0,
            step=1.0,
            format="%.4f",
            key=f"spl_b_{i}"
        )

        nilai_b = sp.Rational(
            str(nilai_b)
        ).limit_denominator(100000)

        b_data.append(
            nilai_b
        )

    b = sp.Matrix(
        b_data
    )

    if st.button(
        "Selesaikan SPL",
        key="btn_spl"
    ):

        st.subheader(
            "Bentuk Sistem Persamaan"
        )

        tampilkan_spl(
            A,
            b
        )

        augmented = A.row_join(
            b
        )

        st.subheader(
            "Matriks Augmented"
        )

        st.latex(
            sp.latex(augmented)
        )

        hasil_rref, langkah = rref_dengan_langkah(
            augmented
        )

        st.subheader(
            "Langkah Gauss-Jordan"
        )

        if len(langkah) == 0:

            st.info(
                "Tidak ada operasi baris "
                "yang diperlukan."
            )

        else:

            for nomor, langkah_text in enumerate(
                langkah,
                start=1
            ):

                st.write(
                    f"**Langkah {nomor}:** "
                    f"{langkah_text}"
                )

        st.subheader(
            "Matriks RREF"
        )

        st.latex(
            sp.latex(hasil_rref)
        )

        st.subheader(
            "Hasil Penyelesaian"
        )

        rank_A = A.rank()

        rank_augmented = augmented.rank()

        if rank_A < rank_augmented:

            st.error(
                "SPL tidak memiliki solusi."
            )

        elif rank_A < int(jumlah_variabel):

            st.warning(
                "SPL memiliki tak hingga "
                "banyak solusi."
            )

            st.latex(
                sp.latex(
                    sp.linsolve(
                        (A, b)
                    )
                )
            )

        else:

            solusi = sp.linsolve(
                (A, b)
            )

            st.success(
                "SPL memiliki solusi tunggal."
            )

            st.latex(
                sp.latex(solusi)
        )
