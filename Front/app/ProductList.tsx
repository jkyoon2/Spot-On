export type ProductInfo = {
    productName: string,
    productImage: string
}

const server = "http://165.132.46.86:32073";

function ProductBlock(productInfo: ProductInfo) {
    return (
        <div className="product" key={productInfo.productImage}>
            <img
                src={server + productInfo.productImage}
                alt="product image"
            />
            <h2>{productInfo.productName}</h2>
        </div>
    )
}

export default function ProductList({ productList }: { productList: ProductInfo[] }) {
    return (
        <>
            {productList.map(ProductBlock)}
        </>
    )
}