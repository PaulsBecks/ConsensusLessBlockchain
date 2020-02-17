import rsa from "js-crypto-rsa";
import keyutils from "js-crypto-key-utils";

export default async function createWallet() {
  const key = await rsa.generateKey(2048);
  let pem_pub_key = await new keyutils.Key("jwk", key.publicKey).export("pem");

  return {
    publicKey: key.publicKey,
    transactions: [],
    privateKey: key.privateKey,
    pem_pub_key
  };
}
