import streamlit as st
import numpy as np
import pandas as pd

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Kalkulator Matriks",
    page_icon="🔢",
    layout="centered"
)

st.title("🔢 Kalkulator Matriks")

st.write(
    "Aplikasi untuk menghitung operasi dasar matriks "
    "menggunakan Python."
)

st.divider()


# =========================================================
# FUNGSI MEMBUAT INPUT MATRIKS
# =========================================================

def buat_matriks(nama, baris, kolom, key):

    st.subheader(nama)

    # Membuat matriks awal berisi angka 0
    data_awal = np.zeros((baris, kolom))

    # Nama baris dan kolom
    nama_baris = [
        f"Baris {i + 1}"
        for i in range(baris)
    ]

    nama_kolom = [
        f"Kolom {j + 1}"
        for j in range(kolom)
    ]

    dataframe_awal = pd.DataFrame(
        data_awal,
        index=nama_baris,
        columns=nama_kolom
    )

    # Tabel yang dapat diedit
    data = st.data_editor(
        dataframe_awal,
        key=key,
        use_container_width=True,
        num_rows="fixed"
    )

    return data.to_numpy(dtype=float)


# =========================================================
# FUNGSI FORMAT ANGKA
# =========================================================

def angka(nilai):

    if abs(nilai) < 1e-10:
        nilai = 0

    if float(nilai).is_integer():
        return str(int(nilai))

    return f"{nilai:.4f}"


# =========================================================
# FUNGSI LANGKAH PENJUMLAHAN
# =========================================================

def langkah_penjumlahan(A, B, hasil):

    st.subheader("📚 Langkah-Langkah Penjumlahan")

    st.write(
        "Penjumlahan matriks dilakukan dengan "
        "menjumlahkan elemen yang berada pada posisi yang sama."
    )

    st.latex(
        r"C=A+B"
    )

    st.write("### 1. Matriks yang digunakan")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.latex(
        r"B="
        + latex_matriks(B)
    )

    st.write("### 2. Perhitungan setiap elemen")

    for i in range(A.shape[0]):

        for j in range(A.shape[1]):

            st.latex(
                rf"""
                C_{{{i+1}{j+1}}}
                =
                {angka(A[i, j])}
                +
                {angka(B[i, j])}
                =
                {angka(hasil[i, j])}
                """
            )

    st.write("### 3. Hasil akhir")

    st.latex(
        r"C="
        + latex_matriks(hasil)
    )


# =========================================================
# FUNGSI LANGKAH PENGURANGAN
# =========================================================

def langkah_pengurangan(A, B, hasil):

    st.subheader("📚 Langkah-Langkah Pengurangan")

    st.write(
        "Pengurangan matriks dilakukan dengan "
        "mengurangkan elemen yang berada pada posisi yang sama."
    )

    st.latex(
        r"C=A-B"
    )

    st.write("### 1. Matriks yang digunakan")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.latex(
        r"B="
        + latex_matriks(B)
    )

    st.write("### 2. Perhitungan setiap elemen")

    for i in range(A.shape[0]):

        for j in range(A.shape[1]):

            st.latex(
                rf"""
                C_{{{i+1}{j+1}}}
                =
                {angka(A[i, j])}
                -
                {angka(B[i, j])}
                =
                {angka(hasil[i, j])}
                """
            )

    st.write("### 3. Hasil akhir")

    st.latex(
        r"C="
        + latex_matriks(hasil)
    )


# =========================================================
# FUNGSI LANGKAH PERKALIAN
# =========================================================

def langkah_perkalian(A, B, hasil):

    st.subheader("📚 Langkah-Langkah Perkalian")

    st.write(
        "Perkalian matriks dilakukan dengan mengalikan "
        "setiap baris Matriks A dengan setiap kolom Matriks B."
    )

    st.latex(
        r"C=A\times B"
    )

    st.write("### 1. Matriks yang digunakan")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.latex(
        r"B="
        + latex_matriks(B)
    )

    st.write("### 2. Perhitungan setiap elemen")

    baris_A = A.shape[0]
    kolom_A = A.shape[1]
    kolom_B = B.shape[1]

    for i in range(baris_A):

        for j in range(kolom_B):

            bagian = []

            for k in range(kolom_A):

                bagian.append(
                    f"({angka(A[i, k])})"
                    f"({angka(B[k, j])})"
                )

            perhitungan = " + ".join(bagian)

            st.latex(
                rf"""
                C_{{{i+1}{j+1}}}
                =
                {perhitungan}
                =
                {angka(hasil[i, j])}
                """
            )

    st.write("### 3. Hasil akhir")

    st.latex(
        r"C="
        + latex_matriks(hasil)
    )


# =========================================================
# FUNGSI LATEX MATRIKS
# =========================================================

def latex_matriks(A):

    baris = []

    for i in range(A.shape[0]):

        elemen = []

        for j in range(A.shape[1]):

            elemen.append(
                angka(A[i, j])
            )

        baris.append(
            " & ".join(elemen)
        )

    isi = r" \\ ".join(baris)

    return (
        r"\begin{bmatrix}"
        + isi
        + r"\end{bmatrix}"
    )


# =========================================================
# FUNGSI LANGKAH TRANSPOSE
# =========================================================

def langkah_transpose(A, hasil):

    st.subheader("📚 Langkah-Langkah Transpose")

    st.write(
        "Transpose dilakukan dengan mengubah baris "
        "menjadi kolom dan kolom menjadi baris."
    )

    st.write("### 1. Matriks awal")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.write("### 2. Pertukaran baris dan kolom")

    st.latex(
        r"""
        A^T_{ij}=A_{ji}
        """
    )

    st.write(
        "Artinya, elemen baris ke-i kolom ke-j "
        "menjadi elemen baris ke-j kolom ke-i."
    )

    st.write("### 3. Hasil transpose")

    st.latex(
        r"A^T="
        + latex_matriks(hasil)
    )


# =========================================================
# FUNGSI LANGKAH DETERMINAN
# =========================================================

def langkah_determinan(A, hasil):

    st.subheader("📚 Langkah-Langkah Determinan")

    n = A.shape[0]

    st.write("### 1. Matriks awal")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    if n == 1:

        st.write("### 2. Rumus")

        st.latex(
            r"\det(A)=a_{11}"
        )

        st.latex(
            rf"\det(A)={angka(A[0, 0])}"
        )

    elif n == 2:

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        st.write("### 2. Rumus determinan 2 × 2")

        st.latex(
            r"""
            \det(A)=ad-bc
            """
        )

        st.write("### 3. Masukkan nilai")

        st.latex(
            rf"""
            \det(A)
            =
            ({angka(a)})({angka(d)})
            -
            ({angka(b)})({angka(c)})
            """
        )

        st.latex(
            rf"""
            =
            {angka(hasil)}
            """
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

        st.write("### 2. Rumus determinan 3 × 3")

        st.latex(
            r"""
            \det(A)
            =
            a(ei-fh)
            -
            b(di-fg)
            +
            c(dh-eg)
            """
        )

        st.write("### 3. Masukkan nilai")

        st.latex(
            rf"""
            =
            ({angka(a)})
            [({angka(e)})({angka(i)})
            -
            ({angka(f)})({angka(h)})]
            -
            ({angka(b)})
            [({angka(d)})({angka(i)})
            -
            ({angka(f)})({angka(g)})]
            +
            ({angka(c)})
            [({angka(d)})({angka(h)})
            -
            ({angka(e)})({angka(g)})]
            """
        )

        st.write("### 4. Hasil")

        st.latex(
            rf"""
            \det(A)={angka(hasil)}
            """
        )

    else:

        st.write(
            "Untuk matriks berukuran lebih dari 3 × 3, "
            "perhitungan dilakukan menggunakan metode "
            "eliminasi/determinasi numerik."
        )

        st.latex(
            rf"""
            \det(A)={angka(hasil)}
            """
        )


# =========================================================
# FUNGSI LANGKAH INVERS
# =========================================================

def langkah_invers(A, hasil, determinan):

    st.subheader("📚 Langkah-Langkah Invers")

    st.write("### 1. Matriks awal")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.write("### 2. Tentukan determinan")

    st.latex(
        rf"""
        \det(A)={angka(determinan)}
        """
    )

    if A.shape == (2, 2):

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        st.write("### 3. Gunakan rumus invers 2 × 2")

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

        st.write("### 4. Masukkan nilai")

        st.latex(
            rf"""
            A^{{-1}}
            =
            \frac{{1}}{{{angka(determinan)}}}
            \begin{{bmatrix}}
            {angka(d)} & {-angka(b)}\\
            {-angka(c)} & {angka(a)}
            \end{{bmatrix}}
            """
        )

    else:

        st.write(
            "Untuk matriks selain 2 × 2, "
            "invers dihitung menggunakan metode "
            "eliminasi Gauss-Jordan."
        )

        st.latex(
            r"""
            [A|I]\rightarrow[I|A^{-1}]
            """
        )

    st.write("### 5. Hasil invers")

    st.latex(
        r"A^{-1}="
        + latex_matriks(hasil)
    )


# =========================================================
# FUNGSI LANGKAH RANK
# =========================================================

def langkah_rank(A, hasil):

    st.subheader("📚 Langkah-Langkah Rank")

    st.write("### 1. Matriks awal")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.write("### 2. Lakukan eliminasi baris")

    st.write(
        "Rank ditentukan dari jumlah baris yang "
        "tidak semuanya bernilai nol setelah "
        "matriks direduksi."
    )

    try:

        _, pivot = np.linalg.qr(A)

        st.write(
            "Perhitungan rank dilakukan secara numerik "
            "menggunakan NumPy."
        )

    except Exception:

        pass

    st.write("### 3. Hasil")

    st.latex(
        rf"""
        \operatorname{{rank}}(A)={hasil}
        """
    )


# =========================================================
# FUNGSI LANGKAH TRACE
# =========================================================

def langkah_trace(A, hasil):

    st.subheader("📚 Langkah-Langkah Trace")

    st.write("### 1. Matriks awal")

    st.latex(
        r"A="
        + latex_matriks(A)
    )

    st.write("### 2. Ambil elemen diagonal utama")

    diagonal = []

    for i in range(A.shape[0]):

        diagonal.append(
            angka(A[i, i])
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
        + "+".join(diagonal)
    )

    st.write("### 3. Hasil")

    st.latex(
        rf"""
        \operatorname{{Tr}}(A)
        =
        {angka(hasil)}
        """
    )


# =========================================================
# PILIH OPERASI
# =========================================================

operasi = st.selectbox(
    "Pilih Operasi Matriks",
    [
        "Penjumlahan",
        "Pengurangan",
        "Perkalian",
        "Transpose",
        "Determinan",
        "Invers",
        "Rank",
        "Trace"
    ]
)


# =========================================================
# UKURAN MATRIKS A
# =========================================================

st.divider()

st.header("Matriks A")

col_a1, col_a2 = st.columns(2)

with col_a1:

    baris_a = st.number_input(
        "Jumlah Baris A",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

with col_a2:

    kolom_a = st.number_input(
        "Jumlah Kolom A",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )


# =========================================================
# INPUT MATRIKS A
# =========================================================

A = buat_matriks(
    "Input Matriks A",
    int(baris_a),
    int(kolom_a),
    "input_A"
)


# =========================================================
# MATRIKS B
# =========================================================

B = None

if operasi in [
    "Penjumlahan",
    "Pengurangan",
    "Perkalian"
]:

    st.divider()

    st.header("Matriks B")

    col_b1, col_b2 = st.columns(2)

    with col_b1:

        baris_b = st.number_input(
            "Jumlah Baris B",
            min_value=1,
            max_value=10,
            value=2,
            step=1
        )

    with col_b2:

        kolom_b = st.number_input(
            "Jumlah Kolom B",
            min_value=1,
            max_value=10,
            value=2,
            step=1
        )

    # -----------------------------------------------------
    # Informasi syarat operasi
    # -----------------------------------------------------

    if operasi == "Penjumlahan":

        st.info(
            "Syarat penjumlahan: ukuran Matriks A "
            "dan Matriks B harus sama."
        )

    elif operasi == "Pengurangan":

        st.info(
            "Syarat pengurangan: ukuran Matriks A "
            "dan Matriks B harus sama."
        )

    elif operasi == "Perkalian":

        st.info(
            "Syarat perkalian: jumlah kolom A harus "
            "sama dengan jumlah baris B."
        )

    # -----------------------------------------------------
    # INPUT MATRIKS B
    # -----------------------------------------------------

    B = buat_matriks(
        "Input Matriks B",
        int(baris_b),
        int(kolom_b),
        "input_B"
    )


# =========================================================
# TOMBOL HITUNG
# =========================================================

st.divider()

hitung = st.button(
    "🔢 HITUNG",
    type="primary",
    use_container_width=True
)


# =========================================================
# PERHITUNGAN
# =========================================================

if hitung:

    # =====================================================
    # PENJUMLAHAN
    # =====================================================

    if operasi == "Penjumlahan":

        if A.shape != B.shape:

            st.error(
                f"Penjumlahan tidak dapat dilakukan. "
                f"Ukuran A = {A.shape[0]}×{A.shape[1]}, "
                f"sedangkan ukuran B = {B.shape[0]}×{B.shape[1]}."
            )

        else:

            hasil = A + B

            st.success(
                "Penjumlahan berhasil!"
            )

            st.subheader(
                "Hasil A + B"
            )

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True,
                hide_index=True
            )

            # LANGKAH
            langkah_penjumlahan(
                A,
                B,
                hasil
            )


    # =====================================================
    # PENGURANGAN
    # =====================================================

    elif operasi == "Pengurangan":

        if A.shape != B.shape:

            st.error(
                f"Pengurangan tidak dapat dilakukan. "
                f"Ukuran A = {A.shape[0]}×{A.shape[1]}, "
                f"sedangkan ukuran B = {B.shape[0]}×{B.shape[1]}."
            )

        else:

            hasil = A - B

            st.success(
                "Pengurangan berhasil!"
            )

            st.subheader(
                "Hasil A - B"
            )

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True,
                hide_index=True
            )

            # LANGKAH
            langkah_pengurangan(
                A,
                B,
                hasil
            )


    # =====================================================
    # PERKALIAN
    # =====================================================

    elif operasi == "Perkalian":

        if A.shape[1] != B.shape[0]:

            st.error(
                "Perkalian tidak dapat dilakukan."
            )

            st.warning(
                f"Kolom A = {A.shape[1]}, "
                f"sedangkan baris B = {B.shape[0]}."
            )

            st.write(
                "Syarat perkalian adalah:"
            )

            st.latex(
                r"\text{kolom A} = \text{baris B}"
            )

        else:

            hasil = A @ B

            st.success(
                "Perkalian berhasil!"
            )

            st.subheader(
                "Hasil A × B"
            )

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True,
                hide_index=True
            )

            st.write(
                f"Ukuran hasil: "
                f"{hasil.shape[0]} × "
                f"{hasil.shape[1]}"
            )

            # LANGKAH
            langkah_perkalian(
                A,
                B,
                hasil
            )


    # =====================================================
    # TRANSPOSE
    # =====================================================

    elif operasi == "Transpose":

        hasil = A.T

        st.success(
            "Transpose berhasil!"
        )

        st.subheader(
            "Transpose Matriks A"
        )

        st.dataframe(
            pd.DataFrame(hasil),
            use_container_width=True,
            hide_index=True
        )

        st.write(
            f"Ukuran awal: "
            f"{A.shape[0]} × "
            f"{A.shape[1]}"
        )

        st.write(
            f"Ukuran transpose: "
            f"{hasil.shape[0]} × "
            f"{hasil.shape[1]}"
        )

        # LANGKAH
        langkah_transpose(
            A,
            hasil
        )


    # =====================================================
    # DETERMINAN
    # =====================================================

    elif operasi == "Determinan":

        if baris_a != kolom_a:

            st.error(
                "Determinan hanya dapat dihitung "
                "untuk matriks persegi."
            )

            st.write(
                f"Ukuran Matriks A sekarang: "
                f"{int(baris_a)} × "
                f"{int(kolom_a)}"
            )

        else:

            hasil = np.linalg.det(A)

            st.success(
                "Determinan berhasil dihitung!"
            )

            st.subheader(
                "Determinan Matriks A"
            )

            st.write(
                f"Ukuran A = "
                f"{int(baris_a)} × "
                f"{int(kolom_a)}"
            )

            st.latex(
                rf"\det(A) = {hasil:.4f}"
            )

            # LANGKAH
            langkah_determinan(
                A,
                hasil
            )


    # =====================================================
    # INVERS
    # =====================================================

    elif operasi == "Invers":

        if baris_a != kolom_a:

            st.error(
                "Invers hanya dapat dihitung "
                "untuk matriks persegi."
            )

        else:

            determinan = np.linalg.det(A)

            if abs(determinan) < 1e-10:

                st.error(
                    "Matriks A tidak mempunyai invers "
                    "karena determinannya = 0."
                )

            else:

                hasil = np.linalg.inv(A)

                st.success(
                    "Invers Matriks A berhasil dihitung!"
                )

                st.subheader(
                    "A⁻¹"
                )

                st.dataframe(
                    pd.DataFrame(hasil),
                    use_container_width=True,
                    hide_index=True
                )

                # LANGKAH
                langkah_invers(
                    A,
                    hasil,
                    determinan
                )


    # =====================================================
    # RANK
    # =====================================================

    elif operasi == "Rank":

        hasil = np.linalg.matrix_rank(A)

        st.success(
            "Rank berhasil dihitung!"
        )

        st.subheader(
            "Rank Matriks A"
        )

        st.latex(
            rf"\operatorname{{rank}}(A) = {hasil}"
        )

        # LANGKAH
        langkah_rank(
            A,
            hasil
        )


    # =====================================================
    # TRACE
    # =====================================================

    elif operasi == "Trace":

        if baris_a != kolom_a:

            st.error(
                "Trace hanya dapat dihitung "
                "untuk matriks persegi."
            )

        else:

            hasil = np.trace(A)

            st.success(
                "Trace berhasil dihitung!"
            )

            st.subheader(
                "Trace Matriks A"
            )

            st.latex(
                rf"\operatorname{{Tr}}(A) = {hasil:g}"
            )

            # LANGKAH
            langkah_trace(
                A,
                hasil
            )


# =========================================================
# INFORMASI APLIKASI
# =========================================================

st.divider()

st.caption(
    "Kalkulator Matriks | "
    "Python + Streamlit + NumPy + Pandas"
        )
