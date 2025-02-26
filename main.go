package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"syscall/js"
)

// readInt64 reads an int64 from a buffer
func readInt64(buf *bytes.Buffer) (int64, error) {
	var value int64
	err := binary.Read(buf, binary.LittleEndian, &value)
	return value, err
}

// readBufferWasm reads multiple Length-Timestamp-Buffer records from a binary buffer
func readBufferWasm(this js.Value, args []js.Value) interface{} {
	// Get binary data from JS Uint8Array
	data := make([]byte, args[0].Length())
	js.CopyBytesToGo(data, args[0])
	buf := bytes.NewBuffer(data)

	// Store parsed records
	var records []interface{}

	// Loop to read multiple records
	for buf.Len() > 0 {
		// Read payload size
		if buf.Len() < 8 {
			fmt.Println("Corrupt data: missing payload size")
			break
		}
		payloadSize, err := readInt64(buf)
		if err != nil {
			fmt.Println("Failed to read payload size:", err)
			break
		}

		// Read timestamp
		if buf.Len() < 8 {
			fmt.Println("Corrupt data: missing timestamp")
			break
		}
		timestamp, err := readInt64(buf)
		if err != nil {
			fmt.Println("Failed to read timestamp:", err)
			break
		}

		// Read value (remaining bytes of this record)
		valueSize := int(payloadSize - 8) // Exclude timestamp size
		if buf.Len() < valueSize {
			fmt.Println("Corrupt data: missing value bytes")
			break
		}
		value := buf.Next(valueSize) // Efficiently extract bytes

		// Create a Uint8Array in JavaScript and copy bytes into it
		jsArray := js.Global().Get("Uint8Array").New(len(value))
		js.CopyBytesToJS(jsArray, value)

		// Create JS object representation
		record := map[string]interface{}{
			"timestamp": timestamp,
			"value":     jsArray, // Return Uint8Array to JS
		}

		records = append(records, record)
	}

	// Return parsed records to JavaScript
	return records
}

// Expose function to JavaScript
func main() {
	js.Global().Set("readBufferWasm", js.FuncOf(readBufferWasm))
	select {} // Keep WASM running
}
