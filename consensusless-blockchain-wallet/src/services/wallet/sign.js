import rsa from "js-crypto-rsa"; // for npm
import { str2ab } from "../strAb";
export default async function(transaction, wallet) {
  const sig = await rsa.sign(
    str2ab(transaction),
    wallet.privateKey,
    "SHA-256",
    {
      name: "RSA-PSS", // default. 'RSASSA-PKCS1-v1_5' is also available.
      saltLength: 64
    }
  );

  const valid = await rsa.verify(
    str2ab(transaction),
    sig,
    wallet.publicKey,
    "SHA-256",
    { name: "RSA-PSS", saltLength: 64 }
  );
  return sig;
}
