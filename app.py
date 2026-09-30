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
# FUNGSI FORMAT ANGKA
# =========================================================

def angka(nilai):
    """Mengubah angka agar lebih rapi saat ditampilkan."""
    nilai = float(nilai)

    if abs(nilai) < 1e-10:
        nilai = 0

    if nilai.is_integer():
        return str(int(nilai))

    return f"{nilai:.4f}"


# =========================================================
# FUNGSI MEMBUAT INPUT MATRIKS
# =========================================================

def buat_matriks(nama, baris, kolom, key):

    st.subheader(nama)

    # Matriks awal berisi angka 0
    data_awal = np.zeros((baris, kolom))

    # Nama baris dan kolom
    nama_baris = [f"Baris {i + 1}" for i in range(baris)]
    nama_kolom = [f"Kolom {j + 1}" for j in range(kolom)]

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
# FUNGSI MENAMPILKAN MATRIKS DALAM LATEX
# =========================================================

def latex_matriks(A):

    baris = []

    for row in A:
        isi = " & ".join(angka(x) for x in row)
        baris.append(isi)

    return (
        r"\begin{bmatrix}"
        + r" \\ ".join(baris)
        + r"\end{bmatrix}"
    )


# =========================================================
# FUNGSI GAUSS-JORDAN
# =========================================================

def gauss_jordan(A):

    A = np.array(A, dtype=float)

    n = A.shape[0]

    # Membuat matriks augmented [A | I]
    augmented = np.hstack(
        (A.copy(), np.eye(n))
    )

    langkah = []

    # Simpan kondisi awal
    langkah.append(
        {
            "operasi": "Matriks augmented awal [A | I]",
            "matriks": augmented.copy()
        }
    )

    for kolom in range(n):

        # -------------------------------------------------
        # Mencari pivot
        # -------------------------------------------------

        pivot_row = kolom

        for i in range(kolom, n):
            if abs(augmented[i, kolom]) > abs(
                augmented[pivot_row, kolom]
            ):
                pivot_row = i

        # Jika pivot nol, matriks tidak memiliki invers
        if abs(augmented[pivot_row, kolom]) < 1e-10:
            return None, langkah

        # -------------------------------------------------
        # Tukar baris jika diperlukan
        # -------------------------------------------------

        if pivot_row != kolom:

            augmented[[kolom, pivot_row]] = \
                augmented[[pivot_row, kolom]]

            langkah.append(
                {
                    "operasi": (
                        f"R{kolom + 1} ↔ R{pivot_row + 1}"
                    ),
                    "matriks": augmented.copy()
                }
            )

        # -------------------------------------------------
        # Membuat pivot menjadi 1
        # -------------------------------------------------

        pivot = augmented[kolom, kolom]

        if abs(pivot - 1) > 1e-10:

            augmented[kolom] = \
                augmented[kolom] / pivot

            langkah.append(
                {
                    "operasi": (
                        f"R{kolom + 1} ← "
                        f"R{kolom + 1} / {angka(pivot)}"
                    ),
                    "matriks": augmented.copy()
                }
            )

        # -------------------------------------------------
        # Membuat elemen lain pada kolom menjadi 0
        # -------------------------------------------------

        for i in range(n):

            if i == kolom:
                continue

            faktor = augmented[i, kolom]

            if abs(faktor) > 1e-10:

                augmented[i] = (
                    augmented[i]
                    - faktor * augmented[kolom]
                )

                langkah.append(
                    {
                        "operasi": (
                            f"R{i + 1} ← R{i + 1} "
                            f"- ({angka(faktor)})R{kolom + 1}"
                        ),
                        "matriks": augmented.copy()
                    }
                )

    # Bagian kanan merupakan invers
    invers = augmented[:, n:]

    return invers, langkah


# =========================================================
# FUNGSI MENAMPILKAN LANGKAH GAUSS-JORDAN
# =========================================================

def tampilkan_gauss_jordan(langkah):

    st.subheader("📐 Langkah Metode Gauss-Jordan")

    st.write(
        "Metode Gauss-Jordan mencari invers dengan mengubah "
        "matriks augmented [A | I] menjadi [I | A⁻¹]."
    )

    for i, data in enumerate(langkah):

        st.markdown(
            f"### Langkah {i + 1}"
        )

        st.latex(
            rf"\text{{Operasi: }} {data['operasi']}"
        )

        matriks = data["matriks"]

        # Membuat tampilan dengan garis pemisah
        teks_baris = []

        n_kolom = matriks.shape[1] // 2

        for row in matriks:

            kiri = " & ".join(
                angka(x) for x in row[:n_kolom]
            )

            kanan = " & ".join(
                angka(x) for x in row[n_kolom:]
            )

            teks_baris.append(
                kiri + r" \mid " + kanan
            )

        latex = (
            r"\left["
            r"\begin{array}{"
            + "c" * n_kolom
            + r"|"
            + "c" * n_kolom
            + r"}"
            + r" \\ ".join(teks_baris)
            + r"\end{array}"
            r"\right]"
        )

        st.latex(latex)


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
        "Gauss-Jordan",
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
                f"sedangkan ukuran B = "
                f"{B.shape[0]}×{B.shape[1]}."
            )

        else:

            hasil = A + B

            st.success("Penjumlahan berhasil!")

            st.subheader("Hasil A + B")

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True,
                hide_index=True
            )

            # Langkah
            st.subheader("📖 Langkah Perhitungan")

            st.latex(
                latex_matriks(A)
                + "+"
                + latex_matriks(B)
                + "="
                + latex_matriks(hasil)
            )


    # =====================================================
    # PENGURANGAN
    # =====================================================

    elif operasi == "Pengurangan":

        if A.shape != B.shape:

            st.error(
                f"Pengurangan tidak dapat dilakukan. "
                f"Ukuran A = {A.shape[0]}×{A.shape[1]}, "
                f"sedangkan ukuran B = "
                f"{B.shape[0]}×{B.shape[1]}."
            )

        else:

            hasil = A - B

            st.success("Pengurangan berhasil!")

            st.subheader("Hasil A - B")

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True,
                hide_index=True
            )

            st.subheader("📖 Langkah Perhitungan")

            st.latex(
                latex_matriks(A)
                + "-"
                + latex_matriks(B)
                + "="
                + latex_matriks(hasil)
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

            st.success("Perkalian berhasil!")

            st.subheader("Hasil A × B")

            st.dataframe(
                pd.DataFrame(hasil),
                use_container_width=True,
                hide_index=True
            )

            st.write(
                f"Ukuran hasil: "
                f"{hasil.shape[0]} × {hasil.shape[1]}"
            )

            st.subheader("📖 Langkah Perhitungan")

            for i in range(A.shape[0]):

                for j in range(B.shape[1]):

                    perkalian = []

                    for k in range(A.shape[1]):

                        perkalian.append(
                            f"{angka(A[i, k])}"
                            f"({angka(B[k, j])})"
                        )

                    rumus = " + ".join(perkalian)

                    st.latex(
                        rf"C_{{{i + 1}{j + 1}}}"
                        rf" = {rumus}"
                        rf" = {angka(hasil[i, j])}"
                    )


    # =====================================================
    # TRANSPOSE
    # =====================================================

    elif operasi == "Transpose":

        hasil = A.T

        st.success("Transpose berhasil!")

        st.subheader("Transpose Matriks A")

        st.dataframe(
            pd.DataFrame(hasil),
            use_container_width=True,
            hide_index=True
        )

        st.write(
            f"Ukuran awal: "
            f"{A.shape[0]} × {A.shape[1]}"
        )

        st.write(
            f"Ukuran transpose: "
            f"{hasil.shape[0]} × {hasil.shape[1]}"
        )

        st.subheader("📖 Langkah Perhitungan")

        st.write(
            "Baris pada Matriks A berubah menjadi "
            "kolom pada matriks transpose."
        )

        st.latex(
            latex_matriks(A)
            + r"^{T}="
            + latex_matriks(hasil)
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
                f"{int(baris_a)} × {int(kolom_a)}"
            )

        else:

            hasil = np.linalg.det(A)

            st.success(
                "Determinan berhasil dihitung!"
            )

            st.subheader("Determinan Matriks A")

            st.write(
                f"Ukuran A = "
                f"{int(baris_a)} × {int(kolom_a)}"
            )

            st.latex(
                rf"\det(A) = {angka(hasil)}"
            )

            st.subheader("📖 Langkah Perhitungan")

            if A.shape == (1, 1):

                st.latex(
                    rf"\det(A) = {angka(A[0, 0])}"
                )

            elif A.shape == (2, 2):

                a = A[0, 0]
                b = A[0, 1]
                c = A[1, 0]
                d = A[1, 1]

                st.latex(
                    r"\det(A)=ad-bc"
                )

                st.latex(
                    rf"=({angka(a)})({angka(d)})"
                    rf"-({angka(b)})({angka(c)})"
                )

                st.latex(
                    rf"={angka(a * d)}"
                    rf"-{angka(b * c)}"
                )

                st.latex(
                    rf"={angka(hasil)}"
                )

            else:

                st.write(
                    "Determinan dihitung menggunakan "
                    "perhitungan numerik NumPy."
                )

                st.latex(
                    rf"\det(A)={angka(hasil)}"
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

                st.latex(
                    r"\det(A)=0"
                )

            else:

                hasil = np.linalg.inv(A)

                st.success(
                    "Invers Matriks A berhasil dihitung!"
                )

                st.subheader("A⁻¹")

                st.dataframe(
                    pd.DataFrame(hasil),
                    use_container_width=True,
                    hide_index=True
                )

                st.subheader("📖 Langkah Perhitungan")

                if A.shape == (2, 2):

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
                        A^{{-1}}
                        =
                        \frac{{1}}{{{angka(determinan)}}}
                        \begin{{bmatrix}}
                        {angka(d)} & -({angka(b)})\\
                        -({angka(c)}) & {angka(a)}
                        \end{{bmatrix}}
                        """
                    )

                else:

                    st.write(
                        "Untuk matriks berukuran lebih dari "
                        "2 × 2, invers dapat dicari dengan "
                        "metode Gauss-Jordan."
                    )

                    invers_gj, langkah_gj = gauss_jordan(A)

                    if invers_gj is not None:

                        tampilkan_gauss_jordan(
                            langkah_gj
                        )


    # =====================================================
    # GAUSS-JORDAN
    # =====================================================

    elif operasi == "Gauss-Jordan":

        if baris_a != kolom_a:

            st.error(
                "Metode Gauss-Jordan untuk mencari invers "
                "memerlukan matriks persegi."
            )

            st.write(
                f"Ukuran Matriks A: "
                f"{int(baris_a)} × {int(kolom_a)}"
            )

        else:

            st.subheader("📐 Metode Gauss-Jordan")

            st.write(
                "Metode ini digunakan untuk mencari invers "
                "matriks dengan mengubah:"
            )

            st.latex(
                r"[A \mid I] \rightarrow [I \mid A^{-1}]"
            )

            invers, langkah = gauss_jordan(A)

            if invers is None:

                st.error(
                    "Matriks A tidak mempunyai invers."
                )

                st.write(
                    "Hal ini terjadi karena matriks "
                    "bersifat singular atau determinannya = 0."
                )

            else:

                st.success(
                    "Matriks berhasil diinvers "
                    "dengan metode Gauss-Jordan!"
                )

                tampilkan_gauss_jordan(langkah)

                st.subheader(
                    "✅ Hasil Akhir A⁻¹"
                )

                st.latex(
                    r"A^{-1}="
                    + latex_matriks(invers)
                )

                st.dataframe(
                    pd.DataFrame(invers),
                    use_container_width=True,
                    hide_index=True
            )
    # =====================================================
    # RANK
    # =====================================================

    elif operasi == "Rank":

        hasil = np.linalg.matrix_rank(A)

        st.success(
            "Rank berhasil dihitung!"
        )

        st.subheader("Rank Matriks A")

        st.latex(
            rf"\operatorname{{rank}}(A) = {hasil}"
        )

        st.subheader("📖 Langkah Perhitungan")

        st.write(
            "Rank ditentukan berdasarkan jumlah baris "
            "atau kolom yang bebas linear."
        )

        st.write(
            f"Hasil perhitungan:"
        )

        st.latex(
            rf"\operatorname{{rank}}(A) = {hasil}"
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

            st.subheader("Trace Matriks A")

            st.latex(
                rf"\operatorname{{Tr}}(A) = {angka(hasil)}"
            )

            st.subheader("📖 Langkah Perhitungan")

            diagonal = [
                A[i, i]
                for i in range(A.shape[0])
            ]

            rumus = " + ".join(
                angka(x) for x in diagonal
            )

            st.latex(
                rf"\operatorname{{Tr}}(A)"
                rf" = {rumus}"
            )

            st.latex(
                rf"= {angka(hasil)}"
            )


# =========================================================
# INFORMASI APLIKASI
# =========================================================

st.divider()

st.caption(
    "Kalkulator Matriks | "
    "Python + Streamlit + NumPy + Pandas"
    )
