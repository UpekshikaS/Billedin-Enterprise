// src/pages/InvoiceCreate.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

interface Product {
  id: number;
  name: string;
  price: number;
  stock: number;
}

interface LineItem {
  productId: number;
  name: string;
  quantity: number;
  price: number;
}

export default function InvoiceCreate() {
  const [items, setItems] = useState<LineItem[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [quantity, setQuantity] = useState<number>(1);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const res = await axios.get('http://localhost:5000/api/products', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setProducts(res.data);
      } catch (err) {
        console.error('Failed to load products');
      }
    };
    fetchProducts();
  }, []);

  const addItem = () => {
    const product = products.find((p) => p.id === selectedId);
    if (!product || quantity <= 0) return;

    const existing = items.find((item) => item.productId === product.id);
    if (existing) {
      setItems(
        items.map((item) =>
          item.productId === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      );
    } else {
      setItems([
        ...items,
        {
          productId: product.id,
          name: product.name,
          quantity,
          price: product.price,
        },
      ]);
    }
    setSelectedId(null);
    setQuantity(1);
  };

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const saveInvoice = async () => {
    if (items.length === 0) {
      alert('Add items before saving.');
      return;
    }

    try {
      const token = localStorage.getItem('authToken');
      const res = await axios.post(
        'http://localhost:5000/api/invoices',
        {
          items,
          total_amount: total,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      alert('Invoice saved! Invoice ID: ' + res.data.invoice_id);
      setItems([]); // clear invoice items after saving
    } catch (error) {
      alert('Failed to save invoice. Please try again.');
    }
  };

  const generatePDF = () => {
    const doc = new jsPDF();

    doc.text("Invoice", 14, 20);
    autoTable(doc, {
      head: [["Product", "Quantity", "Price", "Total"]],
      body: items.map((item) => [
        item.name,
        item.quantity,
        `$${item.price.toFixed(2)}`,
        `$${(item.price * item.quantity).toFixed(2)}`,
      ]),
      startY: 30,
    });

    const finalY = (doc as any).lastAutoTable?.finalY || 40;

    doc.text(`Total: $${total.toFixed(2)}`, 14, finalY + 10);
    doc.save("invoice.pdf");
  };

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Create Invoice</h1>

      <div className="mb-4">
        <select
          className="border p-2 mr-2"
          value={selectedId ?? ''}
          onChange={(e) => setSelectedId(Number(e.target.value))}
        >
          <option value="">Select product</option>
          {products.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} (${p.price})
            </option>
          ))}
        </select>
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(parseInt(e.target.value))}
          className="border p-2 mr-2"
          min={1}
        />
        <button
          onClick={addItem}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Item
        </button>
      </div>

      <table className="w-full bg-white rounded shadow mb-4">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-3 text-left">Product</th>
            <th className="p-3 text-left">Quantity</th>
            <th className="p-3 text-left">Price</th>
            <th className="p-3 text-left">Total</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, index) => (
            <tr key={index} className="border-b">
              <td className="p-3">{item.name}</td>
              <td className="p-3">{item.quantity}</td>
              <td className="p-3">${item.price.toFixed(2)}</td>
              <td className="p-3">${(item.price * item.quantity).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="text-right font-bold text-lg">Total: ${total.toFixed(2)}</div>

      <button
        onClick={saveInvoice}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 mt-4"
      >
        Save Invoice
      </button>

      <button
        onClick={generatePDF}
        className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 mt-2"
      >
        Download PDF
      </button>

    </div>
  );
}
